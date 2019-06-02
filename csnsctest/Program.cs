using System;

namespace csnsctest
{
    class Program
    {
        static void Main(string[] args)
        {
            var key1 = NSphereCryptography.Nsc.GenerateKey(10,-1024,1024);
            var key2 = NSphereCryptography.Nsc.GenerateKey(10,-1024,1024);
            var encrypted = NSphereCryptography.Nsc.Encrypt("kiti",key1,key2);

            Console.WriteLine(NSphereCryptography.Nsc.Decrypt(encrypted,key1,key2));
        }
    }
}
