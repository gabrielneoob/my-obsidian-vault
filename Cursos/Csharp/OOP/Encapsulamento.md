- É um princípio que consiste em esconder detalhes de implementação de um componente, expondo apenas operações seguras e que o mantenha em um estado consistente.

- Regra de ouro: o objeto deve sempre estar em um estado consistente, e a própria classe deve garantir isso

![[Pasted image 20260828151415.png]]

Encapsulamento é o princípio de **esconder os detalhes internos de uma classe** e expor apenas o que é necessário através de uma interface controlada. A ideia central é: quem usa a classe não deveria precisar (nem poder) mexer diretamente no estado interno de forma descontrolada.

### O problema que o encapsulamento resolve

No seu código do `Produto`, os campos são públicos:

```csharp
public string nome;
public double preco;
public int quantidade;
```

Isso significa que qualquer código externo pode fazer:

```csharp
var p = new Produto("Camiseta", 49.90, 10);
p.quantidade = -500; // nada impede isso!
p.preco = -10;       // preço negativo, também permitido
```

Isso quebra totalmente o propósito dos métodos `AdicionarProdutos`/`RemoverProdutos` que você criou — eles existem pra controlar o estoque, mas são "burlados" facilmente porque o campo está exposto.

### Como aplicar: `private` + propriedades

A abordagem padrão em C# é tornar os campos `private` e expor **propriedades** controladas:

```csharp
public class Produto
{
    private string nome;
    private double preco;
    private int quantidade;

    public string Nome
    {
        get { return nome; }
        private set { nome = value; }
    }

    public double Preco
    {
        get { return preco; }
        private set
        {
            if (value < 0)
                throw new ArgumentException("Preço não pode ser negativo");
            preco = value;
        }
    }

    public int Quantidade
    {
        get { return quantidade; }
        private set { quantidade = value; }
    }

    public Produto(string nome, double preco, int quantidade)
    {
        Nome = nome;
        Preco = preco;
        Quantidade = quantidade;
        totalCriados++;
    }
}
```

Repare: o `set` é `private`. Isso significa que **só a própria classe** pode alterar `Preco`, `Nome` e `Quantidade` — de fora, só dá pra ler (`get` público).

### Versão simplificada (auto-propriedades)

Se você não precisa de validação customizada em cada campo, não precisa escrever `get`/`set` manualmente com um campo privado por trás — o C# gera isso pra você:

csharp

```csharp
public string Nome { get; private set; }
public double Preco { get; private set; }
public int Quantidade { get; private set; }
```

Isso é exatamente equivalente ao exemplo anterior (o compilador cria o campo privado escondido), só que mais enxuto.

### Alterando o estado só através de métodos controlados

Com os campos protegidos, `AdicionarProdutos` e `RemoverProdutos` passam a ser o **único caminho** para mudar `Quantidade`:

csharp

```csharp
public void AdicionarProdutos(int quantity)
{
    if (quantity < 0)
        throw new ArgumentException("Quantidade a adicionar não pode ser negativa");
    Quantidade += quantity;
}

public void RemoverProdutos(int quantity)
{
    if (quantity > Quantidade)
        throw new InvalidOperationException("Quantidade insuficiente em estoque");
    Quantidade -= quantity;
}
```

Agora ninguém consegue deixar o estoque negativo "por acidente" — a classe **garante suas próprias regras** (isso se chama manter os _invariantes_ da classe).

### Os 4 níveis de acesso em C# (do mais restrito ao mais aberto)

|Modificador|Quem pode acessar|
|---|---|
|`private`|Só dentro da própria classe|
|`protected`|A própria classe + classes que herdam dela|
|`internal`|Qualquer código no mesmo assembly (projeto)|
|`public`|Qualquer código, de qualquer lugar|

Existem combinações também, como `protected internal` e `private protected`, mas os quatro acima cobrem 90% dos casos do dia a dia.

### Por que isso importa na prática

1. **Controle** — a classe decide como seu próprio estado pode mudar, em vez de confiar que quem usa vai "se comportar direito".
2. **Menos bugs** — impossível deixar o objeto em estado inválido (preço negativo, estoque negativo) se as regras estão centralizadas.
3. **Flexibilidade futura** — se um dia você precisar mudar _como_ `Preco` é calculado ou validado internamente, só muda dentro da classe — quem usa `produto.Preco` de fora nem percebe.
4. **Menos acoplamento** — o código externo depende só da _interface pública_ (`Nome`, `Preco`, `AdicionarProdutos`), não da implementação interna.

### Aplicando no seu `Produto` completo

csharp

```csharp
internal class Produto
{
    public string Nome { get; private set; }
    public double Preco { get; private set; }
    public int Quantidade { get; private set; }

    public static int totalCriados;

    public Produto(string nome, double preco, int quantidade)
    {
        Nome = nome;
        Preco = preco;
        Quantidade = quantidade;
        totalCriados++;
    }

    public Produto(string nome, double preco) : this(nome, preco, 5)
    {
    }

    public double ValorTotalEmEstoque() => Quantidade * Preco;

    public void AdicionarProdutos(int quantity)
    {
        Quantidade += quantity;
    }

    public void RemoverProdutos(int quantity)
    {
        if (quantity > Quantidade)
            throw new InvalidOperationException("Quantidade insuficiente em estoque");
        Quantidade -= quantity;
    }

    public override string ToString() => $"{Nome}, $ {Preco.ToString("F2", CultureInfo.InvariantCulture)}";
}
```

Repare que removi o construtor vazio — se `Nome` é obrigatório para o produto fazer sentido, forçar que ele sempre venha por parâmetro é o próprio encapsulamento em ação (protegendo contra estado inválido).