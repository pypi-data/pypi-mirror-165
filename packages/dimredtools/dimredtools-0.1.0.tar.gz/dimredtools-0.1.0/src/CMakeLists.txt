############ Start Version Parsing ##################

file(STRINGS "${CMAKE_CURRENT_SOURCE_DIR}/version.txt" DIMREDTOOLS_VERSION_READ)
foreach(ver ${DIMREDTOOLS_VERSION_READ})
    if (ver MATCHES "(MAJOR|MINOR|PATCH) +([^ ]+)$")
        set(DIMREDTOOLS_VERSION_${CMAKE_MATCH_1} "${CMAKE_MATCH_2}" CACHE INTERNAL "")
    endif()
endforeach()
string(CONCAT DIMREDTOOLS_VERSION
    "${DIMREDTOOLS_VERSION_MAJOR}"
    ".${DIMREDTOOLS_VERSION_MINOR}"
    ".${DIMREDTOOLS_VERSION_PATCH}"
)

set(PROJECT_VERSION "${DIMREDTOOLS_VERSION}")

message("Version is ${PROJECT_VERSION}")

############# End Version Parsing ##################


add_subdirectory(DimRedTools)

if (DRT_BUILD_PYMODULE)
    add_subdirectory(Python)
endif ()
