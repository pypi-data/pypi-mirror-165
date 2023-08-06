#include "DimRedTools/CoverTree.hpp"

namespace dim_red {

CoverTree::CoverTree(const Eigen::Ref<const Matrix> &x, double base, const std::string &metric)
    : data_(x),
      distance_(getMetricByName(metric)),
      base_(base),
      inv_log_base_(1.0 / log(base)),
      root_(build()) {
}

CoverTree::Node CoverTree::build() {
    if (data_.rows() == 0) {
        throw std::invalid_argument("Dataset is empty");
    }
    std::vector<DistanceSet> distance_sets;
    distance_sets.reserve(static_cast<size_t>(data_.rows() - 1));
    std::vector<DistanceSet *> point_set(static_cast<size_t>(data_.rows() - 1));
    std::vector<DistanceSet *> consumed_set;
    double max_distance = 0.0;

    for (int i = 1; i < data_.rows(); ++i) {
        double distance = distance_(data_.row(0), data_.row(i));
        distance_sets.push_back({i, std::vector<double>(1, distance)});
        point_set[static_cast<size_t>(i) - 1] = &distance_sets.back();
        max_distance = std::max(max_distance, distance);
    }

    return batchInsert(0, getScale(max_distance), getScale(max_distance), &point_set,
                       &consumed_set);
}

CoverTree::Node CoverTree::batchInsert(int point, int max_scale, int top_scale,
                                       std::vector<DistanceSet *> *point_set,
                                       std::vector<DistanceSet *> *consumed_set) const {
    if (point_set->empty()) {
        return {point};
    } else {
        int next_scale = std::min(max_scale - 1, getScale(maxDistance(*point_set)));
        if (next_scale == INT_MIN) {  // We have points with distance 0.
            std::vector<Node> children{{point}};
            for (auto set = point_set->crbegin(); set != point_set->crend(); ++set) {
                children.push_back({(*set)->point});
                consumed_set->push_back(*set);
            }
            point_set->clear();
            return {point, 0.0, children};
        } else {
            std::vector<DistanceSet *> far;
            split(max_scale, point_set, &far);  // O(|point_set|)

            Node child = batchInsert(point, next_scale, top_scale, point_set, consumed_set);

            if (point_set->empty()) {
                point_set->insert(point_set->end(), far.begin(), far.end());
                return child;
            } else {
                std::vector<Node> children{child};
                std::vector<DistanceSet *> new_point_set;
                std::vector<DistanceSet *> new_consumed_set;

                while (!point_set->empty()) {  // O(|point_set| * .size())
                    DistanceSet *set = point_set->back();
                    point_set->pop_back();
                    consumed_set->push_back(set);

                    distanceSplit(set->point, max_scale, point_set,
                                  &new_point_set);                               // O(|point_set|)
                    distanceSplit(set->point, max_scale, &far, &new_point_set);  // O(|far|)

                    children.push_back(batchInsert(set->point, next_scale, top_scale,
                                                   &new_point_set, &new_consumed_set));

                    double f_max = getCoverRadius(max_scale);
                    for (DistanceSet *ds : new_point_set) {  // O(|new_point_set|)
                        ds->distances.pop_back();
                        (ds->distances.back() <= f_max ? *point_set : far).push_back(ds);
                    }

                    for (DistanceSet *ds : new_consumed_set) {  // O(|new_point_set|)
                        ds->distances.pop_back();
                        consumed_set->push_back(ds);
                    }

                    new_point_set.clear();
                    new_consumed_set.clear();
                }

                point_set->insert(point_set->end(), far.begin(), far.end());

                return {point, maxDistance(*consumed_set), children};
            }
        }
    }
}

double CoverTree::getCoverRadius(int scale) const {
    return pow(base_, scale);
}

int CoverTree::getScale(double value) const {
    return static_cast<int>(ceil(inv_log_base_ * log(value)));
}

double CoverTree::maxDistance(const std::vector<DistanceSet *> &v) const {
    double max = 0.0;
    for (const DistanceSet *const set : v) {
        max = std::max(max, set->distances.back());
    }
    return max;
}

void CoverTree::split(int max_scale, std::vector<DistanceSet *> *point_set,
                      std::vector<DistanceSet *> *far_set) const {
    double f_max = getCoverRadius(max_scale);
    std::vector<DistanceSet *> new_set;
    for (DistanceSet *ds : *point_set) {
        (ds->distances.back() <= f_max ? new_set : *far_set).push_back(ds);
    }
    *point_set = new_set;
}

void CoverTree::distanceSplit(int new_point, int max_scale, std::vector<DistanceSet *> *point_set,
                              std::vector<DistanceSet *> *new_point_set) const {
    double f_max = getCoverRadius(max_scale);
    std::vector<DistanceSet *> new_set;
    for (DistanceSet *ds : *point_set) {
        double new_distance = distance_(data_.row(new_point), data_.row(ds->point));
        if (new_distance <= f_max) {
            ds->distances.push_back(new_distance);
        }
        (new_distance <= f_max ? *new_point_set : new_set).push_back(ds);
    }
    *point_set = new_set;
}

std::pair<Vector, Vector> CoverTree::query(const Eigen::Ref<const Vector> &point, int k,
                                           bool sort_results) const {
    return search(point, k, 0.0, true, sort_results);
}

std::pair<Vector, Vector> CoverTree::queryRadius(const Eigen::Ref<const Vector> &point,
                                                 double radius, bool sort_results) const {
    return search(point, 1, radius, false, sort_results);
}

std::pair<Vector, Vector> CoverTree::search(const Eigen::Ref<const Vector> &point, int k,
                                            double radius, bool k_nearest,
                                            bool sort_results) const {
    validate(static_cast<int>(data_.rows()), k, radius, k_nearest);
    double current_distance = distance_(data_.row(0), point);

    // If root is the only node.
    if (k_nearest && root_.children.empty()) {
        return {Vector{{current_distance}}, Vector{{0}}};
    }

    std::vector<DistanceNode> current_cover_set{{current_distance, &root_}};
    std::vector<DistanceNode> zero_set;

    NeighborsHeap<double> heap(static_cast<size_t>(k));
    heap.add(DBL_MAX);
    heap.add(current_distance);

    while (!current_cover_set.empty()) {
        std::vector<DistanceNode> next_cover_set;
        for (const DistanceNode &par : current_cover_set) {
            const Node *parent = par.node;
            for (auto child = parent->children.cbegin(); child != parent->children.cend();
                 ++child) {
                current_distance = child == parent->children.cbegin()
                                       ? par.distance
                                       : distance_(data_.row(child->point), point);

                double upper_bound = k_nearest ? heap.peek() : radius;
                if (current_distance <= upper_bound + child->max_distance) {
                    if (k_nearest && child != parent->children.cbegin() &&
                        current_distance < upper_bound) {
                        heap.add(current_distance);
                    }

                    if (!child->children.empty() || current_distance <= upper_bound) {
                        (!child->children.empty() ? next_cover_set : zero_set)
                            .push_back({current_distance, &(*child)});
                    }
                }
            }
        }
        current_cover_set = std::move(next_cover_set);
    }

    std::vector<std::pair<double, int>> neighbors;
    std::vector<std::pair<double, int>> bound_neighbors;
    double upper_bound = k_nearest ? heap.peek() : radius;
    for (const DistanceNode &ds : zero_set) {
        if (ds.distance <= upper_bound) {
            (ds.distance < upper_bound ? neighbors : bound_neighbors)
                .push_back({ds.distance, ds.node->point});
        }
    }
    return processNeighbors(k_nearest ? k : INT_MAX, sort_results, &neighbors, &bound_neighbors);
}

}  // namespace dim_red
