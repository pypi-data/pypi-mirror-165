#include "dimredtools_pybind/dimredtools_pybind.hpp"
#include "dimredtools_pybind/docstring/docstring.hpp"

using dim_red::CoverTree;
using dim_red::docstring::functionDocInject;

PYBIND11_MODULE(dimredtools_pybind, m) {
    m.doc() = "Python binding of DimRedTools";

    /*py::bind_vector<std::vector<double>>(m, "VectorDouble", py::buffer_protocol());
    py::bind_vector<std::vector<int>>(m, "VectorInt", py::buffer_protocol());
    py::bind_vector<std::vector<std::size_t>>(m, "VectorULongInt", py::buffer_protocol());

    m.def("hello", &dim_red::hello, "name"_a, "Says hello to name");
    functionDocInject(m, "hello", {{"name", "The name to say hello with"}});

    // You *can* use function overload with same name, but python documentation doesn't support
    // function overload Here I choose to make multiple function with different names
    m.def("multiply_by_scalar_double", &dim_red::multiplyByScalar<double>, "vec"_a,
          "scalar"_a, "Multiplies a double vector");
    m.def("multiply_by_scalar_int", &dim_red::multiplyByScalar<int>, "vec"_a, "scalar"_a,
          "Multiplies an int vector");
    m.def("multiply_by_scalar_size_t", &dim_red::multiplyByScalar<size_t>, "vec"_a,
          "scalar"_a, "Multiplies a size_t vector");
    functionDocInject(m, "multiply_by_scalar_double",
                                 {{"vec", "A list of double numbers "},
                                  {"scalar", "A scalar number to multiply the list by."}});
    functionDocInject(m, "multiply_by_scalar_int",
                                 {{"vec", "A list of int numbers "},
                                  {"scalar", "A scalar number to multiply the list by."}});
    functionDocInject(m, "multiply_by_scalar_size_t",
                                 {{"vec", "A list of size_t numbers "},
                                  {"scalar", "A scalar number to multiply the list by."}});*/

    py::class_<NearestNeighbors, PyNearestNeighbors>(
        m, "NearestNeighbors",
        "An abstract class for data structures that implement nearest neighbor search.")
        .def("query", &NearestNeighbors::query, "point"_a, "k"_a, "sort_results"_a = true,
             "Retrieves the k-nearest neighbors for the query point.")
        .def("query_radius", &NearestNeighbors::queryRadius, "point"_a, "r"_a,
             "sort_results"_a = false,
             "Retrieves all the neighbors of the query point in the specified radius.");

    py::class_<CoverTree, NearestNeighbors>(m, "CoverTree")
        .def(py::init<const Eigen::Ref<dim_red::Matrix>&, double, const std::string&>(), "x"_a,
             "base"_a = 1.3, "metric"_a = "euclidean");
}
