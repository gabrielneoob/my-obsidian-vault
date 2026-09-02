- Lista é uma estrutura de dados:
	- Homogênea (dados do mesmo tipo)
	- Ordenada (elementos acessados por meio de posições)
	- Inicia vaiza, e seus elementos são alocados sob demanda

- Classe: List
- Namespace: System.Collections.Generic

- Vantagens:
	- Tamanho variável
	- Facilidade para se realizar inserções e deleções

- Desvantagens:
	- Acesso sequencial aos elementos*

- Inserir elemento na lista: Add, insert;
- Tamanho da lista: Count
- Encontrar primeiro ou último elementos da lista que satisfaça um predicado:
	- list.Find, list.FindLast
- Encontrar primeira ou última posição de elemento da lista que satisfaça um predicado: list.FindIndex, list.FindLastIndex
- Filtrar a lista com base em um predicado: list.FindAll
- Remover elementos da lista: Remove, RemoveAll, RemoveAt, RemoveRange

- Assuntos Pendentes:
	- Generics
	- Predicados (lambda)

```c#
namespace Course
{
    class Program
    {
        static public void Main()
        {
            List<string> list = new List<string>();

            List<string> list2 = new List<string> {"Maria", "Alex" };

            list.Add("João");
            list.Add("Alex");
            list.Add("Bob");
            list.Add("Anna");
            list.Insert(0, "Maria");

            //foreach(string obj in list)
            //{
            //    Console.WriteLine(obj);
            //}

            // lambda
            string s1 = list.Find(s => s.StartsWith("A"));
            string s2 = list.FindLast(s => s.StartsWith("A"));


            int s3 = list.FindIndex(s => s.StartsWith("A"));
            int s4 = list.FindLastIndex(s => s.StartsWith("A"));

            //Console.WriteLine(s1);
            //Console.WriteLine(s2);
            List<string> list3 = list.FindAll(x => x.Length == 4);
            foreach(string obj in list3)
            {
                Console.WriteLine(obj);
            }

            list.Remove("Alex");
        }
  
    }
}
```

```c#
using System.Globalization;

namespace Course
{
    class Program
    {
        static public void Main()
        {
            Console.Write("How many employees will be registered? ");
            int n = int.Parse(Console.ReadLine());

            List<Funcionario> list = new List<Funcionario>();

            for(int i = 0; i < n; i++)
            {
                Console.WriteLine($"Employee #{i + 1}");
                Console.Write("Id: ");
                int id = int.Parse(Console.ReadLine());

                Console.Write("Name: ");
                string nome = Console.ReadLine();

                Console.Write("Salary: ");
                double salario = double.Parse(Console.ReadLine(), CultureInfo.InvariantCulture);

                list.Add(new Funcionario(id, nome, salario));
            }

            foreach (Funcionario obj in list)
            {
                Console.WriteLine($"ID: {obj.Id}, Name: {obj.Name}, Salary: {obj.Salario}");
            }

            Console.Write("Enter the employee id that will have salary increase: ");
            int funcionarioID = int.Parse(Console.ReadLine());

            Funcionario x = list.Find(x => x.Id == funcionarioID);
            double porcentagem;

            if(x == null)
            {
                Console.WriteLine("This id does not exist!");
            } else
            {
                Console.Write("Enter the porcentage: ");
                porcentagem = double.Parse(Console.ReadLine(), CultureInfo.InvariantCulture);
                x.aumentarSalario(porcentagem);
            }

            Console.WriteLine("--------------");

            foreach (Funcionario obj in list)
            {
                Console.WriteLine($"ID: {obj.Id}, Name: {obj.Name}, Salary: {obj.Salario}");
            }
        }
  
    }
}
```