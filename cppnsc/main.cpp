#include <iostream>
#include <string>
#include "nspherecryptography.hpp"
using namespace std;
int main(int argc, char const *argv[])
{
    int key1[] = {-445, -271, 707, -632, 477, -281, -572, 964, 889, -882};
    int key2[] = {-36, 530, 986, 313, -957, -353, -456, 957, 116, 480};
    auto encrypted = encrypt("kiti", key1,key2, 10, 10);
    cout << decrypt(encrypted, key1,key2, 9,10,10) << endl;
    return 0;
}
