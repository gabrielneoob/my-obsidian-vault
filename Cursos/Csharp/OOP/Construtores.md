- É uma operação especial da classe, que executa no momento da instância do objeto

- Usos comuns:
	- Iniciar valores dos atributos
	- Permitir ou obrigar que o objeto receba dados / dependências no momento de sua instância (injeção de dependência)

- Se um construtor customizado não for especificado, a classe disponibiliza o construtor padrão:
	- Produto p = new Produto();

- É possível especificar mais de um construtor na mesma classe (sobrecarga)

Construtores são métodos especiais responsáveis por **inicializar um objeto** no momento em que ele é criado com `new`. Eles têm o mesmo nome da classe e não têm tipo de retorno (nem `void`).

### Construtor padrão (implícito)

Se você não escrever nenhum construtor, o C# gera um automaticamente, sem parâmetros, que apenas inicializa os campos com seus valores padrão (`0`, `null`, `false`, etc.):

```csharp
public class Produto
{
    public string nome;
    public decimal preco;
}

var p = new Produto(); // usa o construtor implícito
// p.nome == null, p.preco == 0
```

⚠️ Assim que você define **qualquer** construtor próprio, o construtor padrão implícito deixa de existir automaticamente.

### Construtor com parâmetros


```csharp
public class Produto
{
    public string nome;
    public decimal preco;

    public Produto(string nome, decimal preco)
    {
        this.nome = nome;
        this.preco = preco;
    }
}

var p = new Produto("Camiseta", 49.90m);
```

Aqui, `this.nome` refere-se ao campo da instância, e `nome` (sem `this`) refere-se ao parâmetro — é preciso o `this` justamente para desambiguar quando os nomes coincidem.

### Sobrecarga de construtores

Uma classe pode ter vários construtores, desde que as assinaturas (tipos/quantidade de parâmetros) sejam diferentes:

```csharp
public class Produto
{
    public string nome;
    public decimal preco;

    public Produto(string nome, decimal preco)
    {
        this.nome = nome;
        this.preco = preco;
    }

    public Produto(string nome) : this(nome, 0m) // encadeamento
    {
    }

    public Produto() : this("Sem nome", 0m)
    {
    }
}
```

O `: this(...)` encadeia um construtor a outro, evitando duplicar lógica de inicialização.

### Construtor estático

Roda **uma única vez**, automaticamente, antes do primeiro uso da classe (seja o primeiro `new`, seja o primeiro acesso a um membro estático). Não recebe parâmetros e não pode ter modificador de acesso:

```csharp
public class Produto
{
    public static int totalCriados;
    public static readonly DateTime DataInicioSistema;

    static Produto()
    {
        DataInicioSistema = DateTime.Now;
        Console.WriteLine("Construtor estático executado!");
    }

    public Produto()
    {
        totalCriados++;
    }
}
```

Serve tipicamente para inicializar campos `static readonly` com lógica mais complexa que uma simples atribuição.

### Encadeamento com a classe base: `base(...)`

Quando há herança, o construtor da classe derivada pode chamar explicitamente um construtor da classe base:

csharp

```csharp
public class Item
{
    public string nome;
    public Item(string nome)
    {
        this.nome = nome;
    }
}

public class Produto : Item
{
    public decimal preco;

    public Produto(string nome, decimal preco) : base(nome)
    {
        this.preco = preco;
    }
}
```

Se você não chamar `base(...)` explicitamente, o C# tenta chamar o construtor **sem parâmetros** da base automaticamente. Se a base não tiver um, dá erro de compilação.

### Construtor privado

Impede que a classe seja instanciada de fora — usado em padrões como Singleton ou em classes só com membros estáticos:

```csharp
public class Configuracao
{
    private static Configuracao instancia;
    public static Configuracao Instancia => instancia ??= new Configuracao();

    private Configuracao() // ninguém de fora pode dar 'new Configuracao()'
    {
    }
}
```

### Inicializador de objeto (não é construtor, mas relacionado)

```csharp
var p = new Produto { nome = "Camiseta", preco = 49.90m };
```

Isso primeiro chama o construtor sem parâmetros (ou o que estiver disponível) e depois atribui as propriedades/campos públicos listados entre `{ }`. É açúcar sintático, não substitui construtor.

### Resumo rápido

|Tipo|Quando roda|Uso típico|
|---|---|---|
|Padrão (implícito)|Se nenhum for definido|Inicialização trivial|
|Com parâmetros|A cada `new`|Garantir estado inicial válido|
|Estático|Uma vez, antes do 1º uso da classe|Inicializar campos `static`|
|Privado|Nunca de fora da classe|Singleton, fábricas internas|
|Encadeado (`this`/`base`)|Conforme chamado|Evitar duplicação de lógica|