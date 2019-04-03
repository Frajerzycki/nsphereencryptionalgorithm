#include <gmpxx.h>
#include <string>
#include <random>
#include <iostream>
#define CLL const long long
#define CI const int
#define CM const mpz_class
#define CC const char

using namespace std;

CI *generate_key(CI length, CI min_inclusive, CI max_inclusive)
{
    int *result = new int[length];
    random_device generator;
    uniform_int_distribution<int> distribution(min_inclusive, max_inclusive);
    for (int i = 0; i < length; i++)
        result[i] = distribution(generator);
    return result;
}

CM sum_of_products(CLL array1[], CI array2[], CI length)
{
    mpz_class sum = 0;
    for (int i = 0; i < length; i++)
        sum += mpz_class(to_string(array1[i])) * mpz_class(array2[i]);
    return sum;
}

CM sum_of_products(CC array1[], CI array2[], CI length)
{
    mpz_class sum = 0;
    for (int i = 0; i < length; i++)
        sum += mpz_class(array1[i]) * mpz_class(array2[i]);    
    return sum;
}

CM sum_of_products(CI array1[], CI array2[], CI length)
{
    mpz_class sum = 0;
    for (int i = 0; i < length; i++)
        sum += mpz_class(array1[i]) * mpz_class(array2[i]);
    return sum;
}

CM sum_of_products(CM array1[], CM array2[], CI length)
{
    mpz_class sum = 0;
    for (int i = 0; i < length; i++)
        sum += array1[i] * array2[i];
    return sum;
}

CM *encrypt(CC message[], CI key1[], CI key2[], CI message_length, CI key1_length, CI key2_length)
{
    CI encrypted_last = message_length << 1;
    auto a = new int[message_length];
    auto e = new mpz_class[message_length];
    auto encrypted = new mpz_class[encrypted_last + 1];

    for (int i = 0; i < message_length; i++)
        a[i] = key1[i % key1_length] - message[i];
    
    CM b = sum_of_products(a, a, message_length),c = sum_of_products(message, a, message_length) << 1;
    for (int i = 0; i < message_length; i++)
        e[i] = b * message[i] - c * a[i];
    for (int i = 1, j = 0; i < encrypted_last; i += 2, j++)
    {
        encrypted[i - 1] = e[j] / b;
        encrypted[i] = e[j] % b + key2[j % key2_length];
    }
    encrypted[encrypted_last] = b;
    return encrypted;
}

CM *encrypt(const string &message, CI key1[], CI key2[], CI key1_length, CI key2_length)
{
    return encrypt(message.c_str(), key1, key2, message.length(), key1_length, key2_length);
}
CC *decrypt(CM *encrypted, CI key1[], CI key2[], CI encrypted_length, CI key1_length, CI key2_length)
{
    CI message_length = encrypted_length >> 1;
    CI encrypted_last = encrypted_length - 1;
    CM b = encrypted[encrypted_last];
    auto e = new mpz_class[message_length];
    auto f = new mpz_class[message_length];
    auto m = new char[message_length];

    for (int i = 1, j = 0; i < encrypted_last; i += 2, j++)
        e[j] = b * encrypted[i - 1] + encrypted[i] - key2[j % key2_length];    
    for (int i = 0; i < message_length; i++)
        f[i] = b*key1[i % key1_length] - e[i];
    
    CM g = sum_of_products(f,f, message_length), h = sum_of_products(f,e, message_length) << 1, d = g*b;
    for (int i = 0; i < message_length; i++) {
        mpz_class result = (g*e[i] - h*f[i])/d;
        m[i] = result.get_si();
    }
    return m;                                 
}
