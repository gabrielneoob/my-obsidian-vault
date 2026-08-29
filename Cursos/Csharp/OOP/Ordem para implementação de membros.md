- Atributos privados;
```c#
	private string _nome;
```
- Propriedades autoimplementadas(auto-properties)
```c#
public double Preco { get; private set; }
public int Quantidade { get; private set; }
```
- Construtores(constructors)
```c#
public Produto()
{
    totalCriados++;
    Quantidade = 0;
}

// Sobrecarga + referenciar outro construtor em um construtor
public Produto(string nome, double preco) : this()
{
    Nome = nome;
    Preco = preco;
}

// Sobrecarga + referenciar outro construtor em um construtor
public Produto(string nome, double preco, int quantidade) : this(nome, preco)
{
    Quantidade = quantidade;
}
```
- propriedades customizadas
```c#
public string Nome
{
    get => _nome;
    set
    {
        if (string.IsNullOrWhiteSpace(value))
            throw new ArgumentException("Nome não pode ser vazio");
        _nome = value;
    }
}
```

- Outros métodos da classe
```c#
        public double ValorTotalEmEstoque()
        {
            return Quantidade * Preco;
        }

        public void AdicionarProdutos(int quantity)
        {
            Quantidade += quantity;
        }

        public void RemoverProdutos(int quantity)
        {
            Quantidade -= quantity;
        }

        public void MostrarProdutoEmEstoque()
        {
            Console.WriteLine($"Dados do produto: {Nome}, ${Preco.ToString("F2", CultureInfo.InvariantCulture)}, {Quantidade}, Total: $ {ValorTotalEmEstoque().ToString("F2", CultureInfo.InvariantCulture)}");
        }

        public override string ToString()
        {
            return Nome + ", $ " + Preco.ToString("F2", CultureInfo.InvariantCulture);
        }
    }
}
```
