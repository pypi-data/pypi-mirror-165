#ifndef DIMREDTOOLS_INCLUDE_DIMREDTOOLS_TESTS__TREETEST_HPP_
#define DIMREDTOOLS_INCLUDE_DIMREDTOOLS_TESTS__TREETEST_HPP_

#include "DimRedTools/DimRedTools.hpp"
#include <iostream>
#include <random>
#include <doctest/doctest.h>

using dim_red::NearestNeighbors;
using dim_red::Matrix;

void compare(const NearestNeighbors &test_tree, const NearestNeighbors &correct_tree,
             const Eigen::Ref<Matrix> &x) {
    std::mt19937 generator(0);
    for (int test = 1; test <= 100; ++test) {
        int i = std::uniform_int_distribution(0, static_cast<int>(x.rows()))(generator);
        std::pair<Eigen::RowVectorXd, Eigen::RowVectorXd> test_answer;
        std::pair<Eigen::RowVectorXd, Eigen::RowVectorXd> correct_answer;
        if (generator() % 2 == 0) {
            int k = std::uniform_int_distribution(1, static_cast<int>(sqrt(x.rows())))(generator);
            std::cout << "Test " << test << ": " << k << " neighbors..." << std::endl;
            test_answer = test_tree.query(x.row(i), k);
            correct_answer = correct_tree.query(x.row(i), k);
        } else {
            double radius = std::uniform_real_distribution(0.0)(generator);
            std::cout << "Test " << test << ": " << radius << " radius..." << std::endl;
            test_answer = test_tree.queryRadius(x.row(i), radius, true);
            correct_answer = correct_tree.queryRadius(x.row(i), radius, true);
        }
        CHECK(test_answer.first.isApprox(correct_answer.first));
        CHECK((test_answer.second == correct_answer.second));
    }
}

#endif  // DIMREDTOOLS_INCLUDE_DIMREDTOOLS_TESTS__TREETEST_HPP_
