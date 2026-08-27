```c#
using System.Runtime.InteropServices;

namespace ConversaoImplicitaECasting
{
    class Program
    {
        static void Main(string[] args)
        {
            // Conversão implícita
            int numeroInteiro = 10;
            double numeroDecimal = numeroInteiro; // Conversão implícita de int para double
            Console.WriteLine($"Número inteiro: {numeroInteiro}");
            Console.WriteLine($"Número decimal (após conversão implícita): {numeroDecimal}");

            // Casting explícito
            double outroNumeroDecimal = 9.78;
            int outroNumeroInteiro = (int)outroNumeroDecimal; // Casting explícito de double para int
            Console.WriteLine($"Outro número decimal: {outroNumeroDecimal}");
            Console.WriteLine($"Outro número inteiro (após casting explícito): {outroNumeroInteiro}");

            double a;
            int b;

            a = 5.1;
            b = (int)a;
     
            Console.WriteLine(b);
        }
    }
}
```
