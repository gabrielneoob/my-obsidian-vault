- Em programação, "vetor" é o nome dado a arranjos unidimensionais
- Arranjo é uma estrutura de dados:
	- Homogênea (dados do mesmo tipo)
	- Ordenada (elementos acessados por meio de posições)
	- Alocada de uma vez só, em um bloco contíguo de memória

- Vantagens:
	- Acesso imediato aos elementos pela sua posição

- Desvantagens:
	- Tamanho fixo
	- Dificuldade para se realizar inserções e deleções
![[Pasted image 20260831115433.png]]

```c#
int n = int.Parse(Console.ReadLine());

double[] vet = new double[n];
double total = 0.00;

for (int i = 0; i < n; i++)
{
    vet[i] = double.Parse(Console.ReadLine(), CultureInfo.InvariantCulture);
    total += vet[i];
}

Console.WriteLine((total / vet.Length).ToString("F2", CultureInfo.InvariantCulture));
```

```c#
using System.Globalization;

namespace Course
{
    class Program
    {
        static public void Main()
        {
            int n = int.Parse(Console.ReadLine());
            Produto[] vet = new Produto[n];
            double precoTotal = 0.00;

            for (int i = 0; i < n; i++)
            {
                string nome = Console.ReadLine();
                double preco = double.Parse(Console.ReadLine(), CultureInfo.InvariantCulture);
                Produto prod = new Produto(nome, preco);
                vet[i] = prod;

                precoTotal += prod.Preco;
            }

            Console.WriteLine($"Preço médio dos produtos: {(precoTotal / vet.Length).ToString("F2", CultureInfo.InvariantCulture)}");
            //foreach (Produto prod in vet)
            //{
            //    Console.WriteLine(prod);
            //}

        }
    }
}
```

```c#
using ComportamentoDeMemoria_Arrays_Listas;
using System.Globalization;

namespace Course
{
    class Program
    {
        static public void Main()
        {
            Estudante[] quarto = new Estudante[10];

            Console.Write("How many rooms will be rented? ");
            int n = int.Parse(Console.ReadLine());

            for(int i = 0; i < n; i++)
            {
                Console.WriteLine($"Rent #{i + 1}: ");
                Console.Write("Name: ");
                string nome = Console.ReadLine();
                Console.Write("Email: ");
                string email = Console.ReadLine();
                Console.Write("Room: ");
                int sala = int.Parse(Console.ReadLine());

                quarto[sala] = new Estudante(nome, email, sala);
            }


            Console.WriteLine("Busy rooms: ");

            for(int i = 0; i < quarto.Length; i++)
            {
                if (quarto[i] != null)
                {
                    Console.WriteLine($"{quarto[i].NumQuarto}: {quarto[i].Nome} {quarto[i].Email}");
                }
            }
        }
    }
}
```

