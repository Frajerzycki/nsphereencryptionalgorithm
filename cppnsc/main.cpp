#include <iostream>
#include "nspherecryptography.hpp"
using namespace std;
int main() {
        const int *key1 = generate_key(10, -1024, 1024);
        const int *key2 = generate_key(10, -1024, 1024);
        const mpz_class *encrypted = encrypt("kiti",key1,key2, 10,10);
        cout << decrypt(encrypted,key1,key2, 9,10,10);
}