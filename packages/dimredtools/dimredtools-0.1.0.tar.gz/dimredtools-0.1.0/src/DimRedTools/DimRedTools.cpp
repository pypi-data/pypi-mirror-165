#include "DimRedTools/DimRedTools.hpp"

namespace dim_red {

Metric getMetricByName(const std::string &name) {
    if (name == "chebyshev") {
        return [](auto &first, auto &second) {
            return (first - second).template lpNorm<Eigen::Infinity>();
        };
    } else if (name == "cityblock" || name == "manhattan" || name == "l1") {
        return [](auto &first, auto &second) { return (first - second).template lpNorm<1>(); };
    } else if (name == "euclidean" || name == "l2") {
        return [](auto &first, auto &second) { return (first - second).norm(); };
    }
    throw std::invalid_argument("Unknown metric: " + name);
}

void NearestNeighbors::validate(int data_size, int k, double radius, bool k_nearest) const {
    if (k <= 0) {
        throw std::invalid_argument("Invalid k: " + std::to_string(k));
    }
    if (k_nearest && k > data_size) {
        throw std::invalid_argument("Neighbor array length is larger than the dataset size");
    }
    if (!k_nearest && radius < 0.0) {
        throw new std::invalid_argument("Invalid radius: " + std::to_string(radius));
    }
}

std::pair<Vector, Vector> NearestNeighbors::processNeighbors(
    int k, bool sort_results, std::vector<std::pair<double, int>> *neighbors,
    std::vector<std::pair<double, int>> *bound_neighbors) const {
    while (!bound_neighbors->empty() && static_cast<int>(neighbors->size()) < k) {
        neighbors->push_back(bound_neighbors->back());
        bound_neighbors->pop_back();
    }
    if (sort_results) {
        std::sort(neighbors->begin(), neighbors->end());
    }
    std::pair<Vector, Vector> result{Vector(neighbors->size()), Vector(neighbors->size())};
    std::transform(neighbors->begin(), neighbors->end(), result.first.begin(),
                   [](auto &result) { return result.first; });
    std::transform(neighbors->begin(), neighbors->end(), result.second.begin(),
                   [](auto &result) { return result.second; });
    return result;
}

Bruteforce::Bruteforce(const Eigen::Ref<const Matrix> &x, const std::string &metric)
    : data_(x), distance_(getMetricByName(metric)) {
    if (x.rows() == 0) {
        throw std::invalid_argument("Dataset is empty");
    }
}

std::pair<Vector, Vector> Bruteforce::query(const Eigen::Ref<const Vector> &point, int k,
                                            bool sort_results) const {
    validate(static_cast<int>(data_.rows()), k, 0.0, true);
    NeighborsHeap<double> heap(static_cast<size_t>(k));
    Vector distances(data_.rows());
    for (int i = 0; i < data_.rows(); ++i) {
        double distance = distance_(data_.row(i), point);
        heap.add(distance);
        distances[i] = distance;
    }

    std::vector<std::pair<double, int>> neighbors;
    std::vector<std::pair<double, int>> bound_neighbors;
    double upper_bound = heap.peek();
    for (int i = 0; i < data_.rows(); ++i) {
        if (distances[i] <= upper_bound) {
            (distances[i] < upper_bound ? neighbors : bound_neighbors).push_back({distances[i], i});
        }
    }
    return processNeighbors(k, sort_results, &neighbors, &bound_neighbors);
}

std::pair<Vector, Vector> Bruteforce::queryRadius(const Eigen::Ref<const Vector> &point,
                                                  double radius, bool sort_results) const {
    validate(static_cast<int>(data_.rows()), 1, radius, false);
    std::vector<std::pair<double, int>> neighbors;
    std::vector<std::pair<double, int>> bound_neighbors;
    for (int i = 0; i < data_.rows(); ++i) {
        double distance = distance_(data_.row(i), point);
        if (distance <= radius) {
            neighbors.push_back({distance, i});
        }
    }
    return processNeighbors(INT_MAX, sort_results, &neighbors, &bound_neighbors);
}

}  // namespace dim_red
