#ifndef DIMREDTOOLS_INCLUDE_DIMREDTOOLS_COVERTREE_HPP_
#define DIMREDTOOLS_INCLUDE_DIMREDTOOLS_COVERTREE_HPP_

#include "DimRedTools.hpp"
#include <cfloat>

namespace dim_red {

/**
 * Cover tree is a data structure for generic nearest neighbor search, which
 * is especially efficient in spaces with small intrinsic dimension. The cover
 * tree has a theoretical bound that is based on the dataset's doubling constant.
 * The bound on search time is O(c<sup>12</sup> log node) where c is the expansion
 * constant of the dataset.
 *
 * <h2>References</h2>
 * <ol>
 * <li> Alina Beygelzimer, Sham Kakade, and John Langford. Cover Trees for Nearest Neighbor. ICML
 * 2006. </li>
 * </ol>
 */
class CoverTree : public NearestNeighbors {
public:
    /**
     * @brief Constructor.
     *
     * @param x the dataset.
     * @param base the base of the expansion constant.
     * @param metric a metric distance measure for nearest neighbor search.
     */
    CoverTree(const Eigen::Ref<const Matrix> &x, double base = 1.3,
              const std::string &metric = "euclidean");

    std::pair<Vector, Vector> query(const Eigen::Ref<const Vector> &point, int k,
                                    bool sort_results = true) const override;

    std::pair<Vector, Vector> queryRadius(const Eigen::Ref<const Vector> &point, double radius,
                                          bool sort_results = false) const override;

private:
    struct Node {
        const int point;
        const double max_distance = 0.0;
        const std::vector<Node> children{};
    };

    struct DistanceSet {
        const int point;
        std::vector<double> distances;
    };

    struct DistanceNode {
        const double distance;
        const Node *node;
    };

    Node build();

    Node batchInsert(int point, int max_scale, int top_scale, std::vector<DistanceSet *> *point_set,
                     std::vector<DistanceSet *> *consumed_set) const;

    double getCoverRadius(int scale) const;

    int getScale(double value) const;

    double maxDistance(const std::vector<DistanceSet *> &v) const;

    void split(int max_scale, std::vector<DistanceSet *> *point_set,
               std::vector<DistanceSet *> *far_set) const;

    void distanceSplit(int new_point, int max_scale, std::vector<DistanceSet *> *point_set,
                       std::vector<DistanceSet *> *new_point_set) const;

    std::pair<Vector, Vector> search(const Eigen::Ref<const Vector> &point, int k, double radius,
                                     bool k_nearest, bool sort_results) const;

    const Eigen::Ref<const Matrix> data_;
    Metric distance_;
    double base_;
    double inv_log_base_;
    Node root_;
};

}  // namespace dim_red

#endif  // DIMREDTOOLS_INCLUDE_DIMREDTOOLS_COVERTREE_HPP_
