using System;
using System.Security.Cryptography;
using System.Numerics;
namespace NSphereCryptography
{
    public static class Nsc
    {
        private static RNGCryptoServiceProvider random_generator = new RNGCryptoServiceProvider();
        public static int[] GenerateKey(int length, int min, int max)
        {
            int[] key = new int[length];
            for (int i = 0; i < length; i++)
            {
                byte[] bytes = new byte[4];
                random_generator.GetBytes(bytes);
                key[i] = (short)new Random(BitConverter.ToInt32(bytes, 0)).Next(min, max);
            }
            return key;
        }

        private static int[] StringToIntArray(String str)
        {
            int[] array = new int[str.Length];
            for (int i = 0; i < str.Length; i++)
                array[i] = (int)str[i];
            return array;
        }


        private static BigInteger SumOfProducts(long[] array1, int[] array2)
        {
            var sum = new BigInteger(0);
            for (int i = 0; i < array1.Length; i++)
                sum += array1[i] * array2[i];
            return sum;
        }

        private static BigInteger SumOfProducts(int[] array1, int[] array2)
        {
            var sum = new BigInteger(0);
            for (int i = 0; i < array1.Length; i++)
                sum += array1[i] * array2[i];
            return sum;
        }

        private static BigInteger SumOfProducts(BigInteger[] array1, BigInteger[] array2)
        {
            var sum = new BigInteger(0);
            for (int i = 0; i < array1.Length; i++)
                sum += array1[i] * array2[i];
            return sum;
        }
        public static BigInteger[] Encrypt(String message, int[] key1, int[] key2)
        {
            var m = StringToIntArray(message);
            var a = new int[m.Length];
            var encryptedLast = m.Length << 1;
            BigInteger[] e = new BigInteger[m.Length], encrypted = new BigInteger[encryptedLast + 1];
            for (int i = 0; i < m.Length; i++)
                a[i] = key1[i % key1.Length] - m[i];
            var b = SumOfProducts(a, a);
            var c = SumOfProducts(m, a) << 1;
            for (int i = 0; i < m.Length; i++)
                e[i] = b * m[i] - a[i] * c;
            for (int i = 1, j = 0; i < encryptedLast; i += 2, j++)
            {
                encrypted[i - 1] = e[j] / b;
                encrypted[i] = e[j] % b + key2[j % key2.Length];
            }
            encrypted[encryptedLast] = b;
            return encrypted;
        }
        public static String Decrypt(BigInteger[] encrypted, int[] key1, int[] key2)
        {
            var messageLength = encrypted.Length >> 1;
            var encryptedLast = encrypted.Length - 1;
            var e = new BigInteger[messageLength];
            var f = new BigInteger[messageLength];
            var m = new char[messageLength];
            var b = encrypted[encryptedLast];
            for (int i = 1, j = 0; i < encryptedLast; i += 2, j++)
                e[j] = b * encrypted[i - 1] + encrypted[i] - key2[j % key2.Length];
            for (int i = 0; i < messageLength; i++)
                f[i] = b * key1[i % key1.Length] - e[i];
            var g = SumOfProducts(f, f);
            var h = SumOfProducts(f, e) << 1;
            var d = g * b;
            for (int i = 0; i < messageLength; i++)
                m[i] = (char)((g * e[i] - f[i] * h) / d);

            return new string(m);
        }
    }
}