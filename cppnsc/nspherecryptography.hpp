#include <gmpxx.h>
#include <string>
#include <random>
#include <iostream>

using namespace std;

const int *generate_key(const int length, const int min_inclusive, const int max_inclusive)
{
    int *result = new int[length];
    random_device generator;
    uniform_int_distribution<int> distribution(min_inclusive, max_inclusive);
    for (int i = 0; i < length; i++)
        result[i] = distribution(generator);
    return result;
}

const mpz_class sum_of_products(const long long array1[], const int array2[], const int length)
{
    mpz_class sum = 0;
    for (int i = 0; i < length; i++)
        sum += mpz_class(to_string(array1[i])) * mpz_class(array2[i]);
    return sum;
}

const mpz_class sum_of_products(const char array1[], const int array2[], const int array1_length, const int array2_length)
{
    mpz_class sum = 0;
    for (int i = 0; i < array1_length; i++)
        sum += mpz_class(array1[i]) * mpz_class(array2[i % array2_length]);    
    return sum;
}

const mpz_class sum_of_products(const int array1[], const int array2[], const int length)
{
    mpz_class sum = 0;
    for (int i = 0; i < length; i++)
        sum += mpz_class(array1[i]) * mpz_class(array2[i]);
    return sum;
}

const mpz_class sum_of_products(const mpz_class array1[], const mpz_class array2[], const int length)
{
    mpz_class sum = 0;
    for (int i = 0; i < length; i++)
        sum += array1[i] * array2[i];
    return sum;
}

const mpz_class *encrypt(const char message[], const int key1[], const int key2[], const int message_length, const int key1_length, const int key2_length)
{
    const int encrypted_last = message_length << 1;
    mpz_class* e = new mpz_class[message_length];
    mpz_class* encrypted = new mpz_class[encrypted_last + 1];
    mpz_class b = 0, c = 0;
    for (int i = 0; i < message_length;i++) {
        const mpz_class value = key1[i % key1_length];
        b += value * value;
        c += message[i] * value;
    }
    c <<= 1;
    for (int i = 0; i < message_length; i++)
        e[i] = b * message[i] - c * key1[i % key1_length];
    for (int i = 1, j = 0; i < encrypted_last; i += 2, j++)
    {
        encrypted[i - 1] = e[j] / b;
        encrypted[i] = e[j] % b + key2[j % key2_length];
    }
    encrypted[encrypted_last] = b;
    return encrypted;
}

const mpz_class *encrypt(const string &message, const int key1[], const int key2[], const int key1_length, const int key2_length)
{
    return encrypt(message.c_str(), key1, key2, message.length(), key1_length, key2_length);
}
const char *decrypt(const mpz_class *encrypted, const int key1[], const int key2[], const int encrypted_length, const int key1_length, const int key2_length)
{
    const int message_length = encrypted_length >> 1;
    const int encrypted_last = encrypted_length - 1;
    const mpz_class b = encrypted[encrypted_last];
    mpz_class* e = new mpz_class[message_length];
    mpz_class* f = new mpz_class[message_length];
    char* m = new char[message_length];

    for (int i = 1, j = 0; i < encrypted_last; i += 2, j++)
        e[j] = b * encrypted[i - 1] + encrypted[i] - key2[j % key2_length];    
    for (int i = 0; i < message_length; i++)
        f[i] = b*key1[i % key1_length];
    
    const mpz_class g = sum_of_products(f,f, message_length), h = sum_of_products(f,e, message_length) << 1, o = g*b;
    for (int i = 0; i < message_length; i++) {
        mpz_class result = (g*e[i] - h*f[i])/o;
        m[i] = result.get_si();
    }
    return m;                                 
}
