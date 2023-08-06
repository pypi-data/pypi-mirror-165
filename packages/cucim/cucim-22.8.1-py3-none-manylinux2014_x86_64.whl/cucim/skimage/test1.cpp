#include <iostream>

int main()
{
    bool is_down = (-3 <= 0);
    bool is_up = !is_down;
    bool is_both = is_down && is_up;
    std::cout << is_down << ", " << is_up << ", " << is_both << std::endl;
    return 0;
}