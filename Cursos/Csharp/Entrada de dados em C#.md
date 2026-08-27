```c#
using System.Globalization;

namespace Course
{
    class Program
    {
        static void Main(string[] args)
        {
            //string frase1 = Console.ReadLine();
            //string frase2 = Console.ReadLine();
            //string frase3 = Console.ReadLine();

            //Console.WriteLine(frase1 + " " + frase2 + " " + frase3);

            //string s = Console.ReadLine();

            //string[] vet = Console.ReadLine().Split(' ');
            //Console.WriteLine(vet[0]);
            //Console.WriteLine(vet[1]);
            //Console.WriteLine(vet[2]);

            //int n1 = int.Parse(Console.ReadLine());
            //char ch = char.Parse(Console.ReadLine());
            //double n2 = double.Parse(Console.ReadLine());

            string[] vet = Console.ReadLine().Split(' ');
            string nome = vet[0];
            char sexo = char.Parse(vet[1]);
            int idade = int.Parse(vet[2]);
            float altura = float.Parse(vet[3], CultureInfo.InvariantCulture);

            Console.WriteLine("Nome: " + nome);
            Console.WriteLine("Sexo: " + sexo);
            Console.WriteLine("idade: " + idade);
            Console.WriteLine("Altura: " + altura.ToString("F2", CultureInfo.InvariantCulture));
        }

    }
}

