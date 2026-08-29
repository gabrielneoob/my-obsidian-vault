- É uma referência para o próprio objeto

- Usos comuns:
	- Diferenciar atributos de variáveis locais (Java)
	- Referenciar outro construtor em um construtor
	- Passar o próprio objeto com argumento na chamada de um método ou construtor

```csharp
using System.Globalization;

namespace OOP
{
    internal class Produto
    {
        public string nome;
        public double preco;
        public int quantidade;

        public static int totalCriados;

        public Produto ()
        {
            totalCriados++;
            this.quantidade = 0;
        }

        // Sobrecarga + referenciar outro construtor em um construtor
        public Produto(string nome, double preco) : this()
        {
            this.nome = nome;
            this.preco = preco;
        }

        // Sobrecarga + referenciar outro construtor em um construtor
        public Produto(string nome, double preco, int quantidade) : this(nome, preco)
        {
            this.quantidade = quantidade;
        }

        public double ValorTotalEmEstoque()
        {
            double totalEmEstoque = quantidade * preco;

            return totalEmEstoque;
        }

        public void AdicionarProdutos(int quantity)
        {
            this.quantidade += quantity;
        }

        public void RemoverProdutos(int quantity)
        {
            this.quantidade -= quantity;
        }

        public void MostrarProdutoEmEstoque()
        {
            Console.WriteLine($"Dados do produto: {this.nome}, ${this.preco.ToString("F2", CultureInfo.InvariantCulture)}, {this.quantidade}, Total: $ {this.ValorTotalEmEstoque().ToString("F2", CultureInfo.InvariantCulture)}");
        }

        public override string ToString()
        {
            return nome + ", $ " + preco.ToString("F2", CultureInfo.InvariantCulture);
        }
    }
}
```
