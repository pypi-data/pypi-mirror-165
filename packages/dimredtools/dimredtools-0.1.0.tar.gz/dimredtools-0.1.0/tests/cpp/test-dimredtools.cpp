#include "doctest/doctest.h"
#include "DimRedTools/DimRedTools.hpp"

using dim_red::NeighborsHeap;
using dim_red::Matrix;
using dim_red::Metric;
using dim_red::getMetricByName;

TEST_SUITE("NeighborsHeap") {
    TEST_CASE("IncorrectLimit") {
        CHECK_THROWS(NeighborsHeap<int>(0));
    }
    TEST_CASE("SimpleUsage") {
        srand(12);
        int limit = 1000;
        NeighborsHeap<int> heap(limit);
        double max_number = 0;
        for (int i = 0; i < 1000; ++i) {
            double next = rand();
            heap.add(next);
            max_number = std::max(max_number, next);
            CHECK_EQ(heap.peek(), max_number);
        }
    }
    TEST_CASE("ExceedingLimit") {
        NeighborsHeap<int> heap(4);
        for (double number : {1, 2, 3, 4, 2}) {
            heap.add(number);
        }
        CHECK_EQ(heap.peek(), 3);
        heap.add(2);
        CHECK_EQ(heap.peek(), 2);
    }
}

TEST_SUITE("Metrics") {
    TEST_CASE("UnknownMetric") {
        CHECK_THROWS(getMetricByName("some_metric"));
    }
    TEST_CASE("chebyshev") {
        Metric chebyshev = getMetricByName("chebyshev");
        CHECK_EQ(chebyshev(Matrix{{1, 0, 0}}, Matrix{{0, 1, 0}}), 1);
        CHECK_EQ(chebyshev(Matrix{{1, 0, 0}}, Matrix{{3, -5, 3}}), 5);
    }
    TEST_CASE("l1") {
        for (const std::string &name : {"l1", "cityblock", "manhattan"}) {
            Metric metric = getMetricByName(name);
            CHECK_EQ(metric(Matrix{{1, 0, 0}}, Matrix{{0, 1, 0}}), 2);
            CHECK_EQ(metric(Matrix{{1, 0, 0}}, Matrix{{3, -5, 3}}), 10);
        }
    }
    TEST_CASE("l2") {
        for (const std::string &name : {"l2", "euclidean"}) {
            Metric metric = getMetricByName(name);
            CHECK_EQ(metric(Matrix{{1, 1, 0}}, Matrix{{0, 1, 0}}), 1);
            CHECK_EQ(metric(Matrix{{1, 0, 0}}, Matrix{{4, -4, 0}}), 5);
        }
    }
}
