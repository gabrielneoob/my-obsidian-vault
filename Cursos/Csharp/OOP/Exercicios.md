```c#
using System.Globalization;

namespace OOP
{
    class Program
    {
        static public void Main()
        {
            Triangulo x, y;

            x = new Triangulo();
            y = new Triangulo();

            Console.WriteLine("Entre com as medidas do triângulo X");
            x.A = double.Parse(Console.ReadLine());
            x.B = double.Parse(Console.ReadLine());
            x.C = double.Parse(Console.ReadLine());

            Console.WriteLine("Entre com as medidas do triângulo Y");
            y.A = double.Parse(Console.ReadLine());
            y.B = double.Parse(Console.ReadLine());
            y.C = double.Parse(Console.ReadLine());

            // Exercicio 1 - Fazer um programa para ler os dados de duas pessoas, depois mostrar o nome da pessoa mais  velha.

            Pessoa p1, p2;

            p1 = new Pessoa();
            p2 = new Pessoa();

            Console.WriteLine("Dados da priemira pessoa:");
            p1.name = Console.ReadLine();
            p1.age = int.Parse(Console.ReadLine());

            Console.WriteLine("Dados da segunda pessoa:");
            p2.name = Console.ReadLine();
            p2.age = int.Parse(Console.ReadLine());


            if (p1.age > p2.age)
            {
                Console.WriteLine($"Pessoa mais velha: {p1.name}");
            }
            else
            {
                Console.WriteLine($"Pessoa mais velha: {p2.name}");
            }

            // Exercicio 2 - Fazer um programa para ler nome e salário de dois funcionários. Depois, mostrar o salário médio dos funcionários.

            //Funcionario x, y;

            //x = new Funcionario();
            //y = new Funcionario();

            //double averageSalary;

            //Console.WriteLine("Dados do primeiro funcionário: ");
            //x.name = Console.ReadLine();
            //x.salary = double.Parse(Console.ReadLine(), CultureInfo.InvariantCulture);

            //Console.WriteLine("Dados do segundo funcionário: ");
            //y.name = Console.ReadLine();
            //y.salary = double.Parse(Console.ReadLine(),CultureInfo.InvariantCulture);

            //averageSalary = (x.salary + y.salary) / 2;

            //Console.WriteLine($"Salário médio = {averageSalary.ToString("F2", CultureInfo.InvariantCulture)}");
        }
    }
}
```
