#include "doctest/doctest.h"
#include <nanobench.h>
#include "DimRedTools/CoverTree.hpp"
#include "DimRedTools/tests/_testdata.hpp"

TEST_CASE("CoverTree_Construction") {
    ankerl::nanobench::Bench().run("CoverTree_1000x10", [&]() {
        Matrix data = testDataset(1000, 10);
        dim_red::CoverTree tree(data);
    });
}
