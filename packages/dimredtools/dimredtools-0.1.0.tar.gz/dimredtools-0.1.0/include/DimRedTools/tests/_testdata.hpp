#ifndef DIMREDTOOLS_SRC_DIMREDTOOLS__TESTDATA_HPP_
#define DIMREDTOOLS_SRC_DIMREDTOOLS__TESTDATA_HPP_

#include "DimRedTools/DimRedTools.hpp"
#include <random>

using dim_red::Matrix;

Matrix testDataset(int samples, int features) {
    std::mt19937 generator(0);
    std::normal_distribution distribution;
    return Matrix::NullaryExpr(samples, features, [&]() { return distribution(generator); });
}

#endif  // DIMREDTOOLS_SRC_DIMREDTOOLS__TESTDATA_HPP_
