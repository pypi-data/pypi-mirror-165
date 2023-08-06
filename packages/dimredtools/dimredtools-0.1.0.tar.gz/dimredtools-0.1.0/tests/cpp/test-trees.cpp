#include <doctest/doctest.h>
#include "DimRedTools/CoverTree.hpp"
#include "DimRedTools/tests/_testdata.hpp"
#include "DimRedTools/tests/_treetest.hpp"

using dim_red::Matrix;
using dim_red::CoverTree;

TEST_SUITE("CoverTree") {
    TEST_CASE("InvalidArguments") {
        Matrix empty{};
        CHECK_THROWS(CoverTree(empty));
        Matrix some_matrix{{1, 2, 3}, {4, 5, 6}};
        CoverTree tree(some_matrix);
        CHECK_THROWS(tree.query(Matrix{{0, 0, 0}}, 0));
        CHECK_THROWS(tree.query(Matrix{{0, 0, 0}}, 3));
        CHECK_THROWS(tree.queryRadius(Matrix{{0, 0, 0}}, -1));
    }
    TEST_CASE("Correctness") {
        Matrix data = testDataset(1000, 10);
        compare(CoverTree(data), dim_red::Bruteforce(data), data);
    }
}
