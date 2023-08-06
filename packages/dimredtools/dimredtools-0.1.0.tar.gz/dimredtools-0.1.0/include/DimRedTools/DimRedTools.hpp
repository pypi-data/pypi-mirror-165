#ifndef DIMREDTOOLS_INCLUDE_DIMREDTOOLS_DIMREDTOOLS_HPP_
#define DIMREDTOOLS_INCLUDE_DIMREDTOOLS_DIMREDTOOLS_HPP_

#include <string>
#include <queue>
#include <functional>
#include <cmath>
#include <stdexcept>
#include <algorithm>
#include <Eigen/Dense>

namespace dim_red {

using Matrix = Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
using Vector = Eigen::RowVectorXd;
using Metric =
    std::function<double(const Eigen::Ref<const Vector> &, const Eigen::Ref<const Vector> &)>;

/**
 * @brief A class for tracking k-nearest neighbors. Implemented as a min-heap with a limited size.
 *
 * @tparam T type of distance (usually double)
 */
template <typename T>
class NeighborsHeap {
public:
    /**
     * @brief Constructor.
     *
     * @param limit the maximum heap size.
     * @throws std::invalid_argument if the limit is less than or equal to zero.
     */
    NeighborsHeap(size_t limit) : limit_(limit) {
        if (limit <= 0) {
            throw std::invalid_argument("Invalid limit: " + std::to_string(limit));
        }
    }

    /**
     * @brief Add a new value. Also remove the largest value if the heap size is exceeding the
     * specified limit.
     *
     * @param value a new value.
     */
    void add(T value) {
        queue_.push(value);
        if (queue_.size() == limit_ + 1) {
            queue_.pop();
        }
    }

    /**
     * @brief Returns the largest value in the heap.
     *
     * @return the largest value.
     */
    const T &peek() const {
        return queue_.top();
    }

private:
    size_t limit_;
    std::priority_queue<T> queue_;
};

/**
 * @brief An abstract class for data structures that implement nearest neighbor search.
 */
class NearestNeighbors {
public:
    virtual ~NearestNeighbors() {
    }

    /**
     * @brief Retrieves the k-nearest neighbors for the query point.
     *
     * @param point the query point.
     * @param k the number of nearest neighbors to search for.
     * @param sort_results if true, the neighbors will be sorted by distances in ascending order.
     * @return the k-nearest neighbors.
     */
    virtual std::pair<Vector, Vector> query(const Eigen::Ref<const Vector> &point, int k,
                                            bool sort_results = true) const = 0;

    /**
     * @brief Retrieves all the neighbors of the query point in the specified radius.
     *
     * @param point the query point.
     * @param radius the search radius.
     * @param sort_results if true, the neighbors will be sorted by distances in ascending order.
     * @return the nearest neighbors in the specified radius.
     */
    virtual std::pair<Vector, Vector> queryRadius(const Eigen::Ref<const Vector> &point,
                                                  double radius,
                                                  bool sort_results = false) const = 0;

protected:
    void validate(int data_size, int k, double radius, bool k_nearest) const;

    std::pair<Vector, Vector> processNeighbors(
        int k, bool sort_results, std::vector<std::pair<double, int>> *neighbors,
        std::vector<std::pair<double, int>> *bound_neighbors) const;
};

/**
 * @brief A bruteforce implementation of nearest neighbor search.
 */
class Bruteforce : public NearestNeighbors {
public:
    /**
     * @brief Constructor.
     *
     * @param x the dataset to search in.
     * @param metric the distance metric.
     */
    Bruteforce(const Eigen::Ref<const Matrix> &x, const std::string &metric = "euclidean");

    std::pair<Vector, Vector> query(const Eigen::Ref<const Vector> &point, int k,
                                    bool sort_results = true) const override;

    std::pair<Vector, Vector> queryRadius(const Eigen::Ref<const Vector> &point, double radius,
                                          bool sort_results = false) const override;

private:
    const Eigen::Ref<const Matrix> data_;
    Metric distance_;
};

/**
 * @brief Returns the function for the metric with the specified name.
 *
 * @param name the name of the metric.
 * @return the corresponding function.
 * @throws std::invalid_argument if the metric is unknown.
 */
Metric getMetricByName(const std::string &name);

}  // namespace dim_red

#endif
