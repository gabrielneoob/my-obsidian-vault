- É um recurso que uma classe possui de oferecer mais de uma operação com o mesmo nome, porém com diferentes listas de parâmetros.

Sobrecarga (_overload_) é a capacidade de ter **vários métodos (ou construtores) com o mesmo nome**, desde que suas **assinaturas** sejam diferentes. O compilador decide qual versão chamar com base nos argumentos que você passa.

### O que define uma assinatura diferente

A assinatura é composta pelo **nome + tipos e quantidade de parâmetros** (o tipo de retorno **não conta**). Então, para sobrecarregar, você precisa variar:

- a **quantidade** de parâmetros, ou
- o **tipo** dos parâmetros, ou
- a **ordem** dos tipos dos parâmetros

csharp

```csharp
public class Calculadora
{
    public int Somar(int a, int b)
    {
        return a + b;
    }

    public double Somar(double a, double b) // tipo diferente
    {
        return a + b;
    }

    public int Somar(int a, int b, int c) // quantidade diferente
    {
        return a + b + c;
    }

    public string Somar(string a, string b) // tipo diferente (concatenação!)
    {
        return a + b;
    }
}
```

Ao chamar, o compilador escolhe automaticamente a versão certa:

```csharp
var calc = new Calculadora();
calc.Somar(2, 3);          // chama Somar(int, int) -> 5
calc.Somar(2.5, 3.1);      // chama Somar(double, double) -> 5.6
calc.Somar(2, 3, 4);       // chama Somar(int, int, int) -> 9
calc.Somar("a", "b");      // chama Somar(string, string) -> "ab"
```

### ⚠️ O que NÃO conta como sobrecarga válida

Mudar **só o tipo de retorno** não é suficiente — o compilador não consegue diferenciar as chamadas, então isso dá **erro de compilação**:

```csharp
public int Somar(int a, int b) { return a + b; }
public double Somar(int a, int b) { return a + b; } // ERRO: mesma assinatura
```

Mudar **só o nome dos parâmetros** também não conta:

```csharp
public int Somar(int a, int b) { ... }
public int Somar(int x, int y) { ... } // ERRO: assinatura idêntica (int, int)
```

### Sobrecarga em construtores (você já viu isso!)

É exatamente o que apareceu no exemplo anterior:

```csharp
public class Produto
{
    public string Nome;
    public decimal Preco;

    public Produto(string nome, decimal preco)
    {
        Nome = nome;
        Preco = preco;
    }

    public Produto(string nome) : this(nome, 0m) // sobrecarga + encadeamento
    {
    }

    public Produto() : this("Sem nome", 0m) // outra sobrecarga
    {
    }
}
```

```csharp
new Produto("Camiseta", 49.90m);
new Produto("Caneca");           // preço vira 0
new Produto();                   // nome vira "Sem nome", preço vira 0
```

### Sobrecarga com `params`

csharp

```csharp
public int Somar(params int[] numeros)
{
    int total = 0;
    foreach (var n in numeros) total += n;
    return total;
}
```

csharp

```csharp
calc.Somar(1, 2);        // funciona
calc.Somar(1, 2, 3, 4);  // funciona, quantidade variável
```

Cuidado: se você tiver `Somar(int, int)` **e** `Somar(params int[])` ao mesmo tempo, o C# prefere a versão mais específica (`Somar(int, int)`) quando possível, e só cai no `params` quando não há correspondência exata.

### Sobrecarga com parâmetros opcionais (alternativa parecida)

Às vezes o que parece precisar de sobrecarga pode ser resolvido com valores padrão:

csharp

```csharp
public int Somar(int a, int b, int c = 0)
{
    return a + b + c;
}
```

csharp

```csharp
calc.Somar(2, 3);     // c assume 0
calc.Somar(2, 3, 4);  // c = 4
```

Isso reduz a necessidade de escrever várias sobrecargas manualmente, mas tem limitações (por exemplo, não sobrecarrega bem quando os tipos mudam).

### Por que isso é útil

- Permite oferecer **a mesma operação lógica** ("somar", "criar produto") de formas convenientes diferentes, sem precisar inventar nomes como `SomarInt`, `SomarDouble`, `SomarTresNumeros`.
- Deixa a API mais **intuitiva** para quem usa a classe — você "adivinha" que existe `Somar` e o compilador acha a versão certa pra você.
- É a base de coisas como `Console.WriteLine(...)`, que tem dezenas de sobrecargas (`string`, `int`, `double`, `object`, `char[]`, etc.) — por isso funciona com praticamente qualquer tipo que você passar.

### Resumo

|Conceito|Vale para sobrecarga?|
|---|---|
|Quantidade de parâmetros diferente|✅ Sim|
|Tipo de parâmetros diferente|✅ Sim|
|Ordem dos tipos diferente|✅ Sim|
|Apenas nome dos parâmetros diferente|❌ Não|
|Apenas tipo de retorno diferente|❌ Não|

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

        }

        public Produto(string nome, double preco, int quantidade)
        {
            this.nome = nome;
            this.preco = preco;
            this.quantidade = quantidade;
            totalCriados++;
        }

        // Sobrecarga
        public Produto(string nome, double preco)
        {
            this.nome = nome;
            this.preco = preco;
            this.quantidade = 5;
            totalCriados++;
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
