#include <iostream>
#include "DimRedTools/DimRedTools.hpp"

int main()
{
    std::string my_name = "Jeremy";
    std::cout << "My Name is " << my_name << std::endl;
    
    // Respond
    std::cout << dim_red::hello(my_name) << std::endl;
}
