#include "DRTConfig.hpp"
#include <string>

namespace dim_red {

std::string getDimRedToolsVersion() {
    return std::string("DimRedTools ") + DIMREDTOOLS_VERSION;
}

}  // namespace dim_red
