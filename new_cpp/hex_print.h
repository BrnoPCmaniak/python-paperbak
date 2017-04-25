// http://stackoverflow.com/a/37250459/2629036
#include <iostream>
#include <iomanip>

template <typename T>
std::string HexToString(T uval)
{
    std::stringstream ss;
    ss << "0x" << std::setw(sizeof(uval) * 2) << std::setfill('0') << std::hex << +uval;
    return ss.str();
}
