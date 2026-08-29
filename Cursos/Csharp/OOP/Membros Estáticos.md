- Também chamados membros de classe
	- Em oposição a membros de instância

- São membros que fazem sentido independentemente de objetos. Não precisam de objeto para serem chamados. São chamados a partir do próprio nome da classe.

- Aplicações comuns:
	- Classes utilitárias, exemplo: Math.Sqrt(double)
	- Declaração de constantes

- Uma classe que possui somente membros estáticos, pode ser uma classe estática também. Esta classe não poderá ser instanciada. 

Membros estáticos em C# são membros (campos, métodos, propriedades, construtores, classes) que pertencem **à classe em si**, e não a uma instância específica dela.

### A diferença fundamental

```csharp
public class Produto
{
    public string nome;           // membro de instância
    public static int totalCriados; // membro estático
}
```

- Cada `new Produto()` cria sua própria cópia de `nome`.
- Já `totalCriados` existe **uma única vez**, compartilhada por todas as instâncias — e também acessível mesmo sem nenhuma instância existir.

### Como se acessa

Membro de instância → através do objeto:

```csharp
Produto p = new Produto();
p.nome = "Camiseta";
```

Membro estático → através do nome da classe (nunca da instância):

```csharp
Produto.totalCriados++;
```

### Exemplo prático combinando com seu código anterior


```csharp
public class Produto
{
    public string nome;
    public decimal preco;
    
    public static int totalCriados; // contador compartilhado

    public Produto(string nome, decimal preco)
    {
        this.nome = nome;
        this.preco = preco;
        totalCriados++; // incrementa o contador global toda vez que um Produto é criado
    }

    public override string ToString()
    {
        return nome + ", $ " + preco.ToString("F2", CultureInfo.InvariantCulture);
    }
}
```

```csharp
var p1 = new Produto("Camiseta", 49.90m);
var p2 = new Produto("Calça", 89.90m);

Console.WriteLine(Produto.totalCriados); // 2
```

### Tipos de membros estáticos

|Tipo|Exemplo|
|---|---|
|Campo estático|`static int totalCriados;`|
|Método estático|`static double Somar(double a, double b)`|
|Propriedade estática|`static string Versao { get; set; }`|
|Construtor estático|`static Produto() { ... }` — roda **uma vez**, antes do primeiro uso da classe|
|Classe estática|`static class Utilitarios { ... }` — só pode conter membros estáticos, nunca é instanciada|

### Métodos estáticos vs. de instância

Um método estático **não pode acessar** membros de instância diretamente, porque não existe um objeto (`this`) associado a ele:

```csharp
public static void Metodo()
{
    // Console.WriteLine(nome); // ERRO — 'nome' não é estático
    Console.WriteLine(totalCriados); // OK — também é estático
}
```

### Onde isso costuma aparecer no dia a dia

- **`Math.Sqrt()`, `Console.WriteLine()`** — métodos estáticos de classes do próprio .NET, você nunca instancia `Math` ou `Console`.
- **Contadores/singletons simples**, como no exemplo do `totalCriados`.
- **Constantes e configurações globais** (`static readonly`).
- **Métodos utilitários/helpers** que não dependem de estado de instância (ex: `Utilitarios.FormatarMoeda(valor)`).
![[Pasted image 20260827204419.png]]