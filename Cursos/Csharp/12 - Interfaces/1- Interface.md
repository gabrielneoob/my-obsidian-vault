- Interface é um tipo que define um conjunto de operações que uma classe (ou struct) deve implementar.

- A interface estabelece um **contrato** que a classe (ou struct) deve cumprir.

```csharp
interface IShape {
	double Area();
	double Perimeter();
}
```

### Interfaces em Csharp##

Uma interface define um **contrato**: um conjunto de membros (métodos, propriedades) que qualquer classe que a implementa é obrigada a fornecer — mas sem nenhuma implementação própria.

#### Sintaxe básica

csharp

```csharp
public interface IShape
{
    double Area(); // sem corpo, sem modificador de acesso (implícito public)
}

public class Circle : IShape
{
    public double Radius { get; set; }

    public double Area() => Math.PI * Radius * Radius;
}

public class Square : IShape
{
    public double Side { get; set; }

    public double Area() => Side * Side;
}
```

- Nome convencionalmente começa com `I` (`IShape`, `IDisposable`, `IEnumerable`).
- Classe usa `:` pra implementar, igual herança — mas pode implementar **várias interfaces** (diferente de classe, que só herda de uma).
- Todo membro da interface tem que ser implementado como `public` na classe.

#### Interface vs Abstract class

Já vimos a diferença de `abstract`/`virtual` — aqui é o próximo nível dessa mesma discussão:

||Interface|Abstract class|
|---|---|---|
|Estado (campos)|Não|Sim|
|Implementação padrão|Não (tradicionalmente)|Sim, pode misturar|
|Herança múltipla|Sim, várias interfaces|Não, só uma classe base|
|Construtor|Não|Sim|
|Quando usar|Contrato de comportamento entre classes não relacionadas|Hierarquia de classes com estado/comportamento compartilhado|

Exemplo clássico de motivo pra usar interface em vez de abstract class: `Duck` e `Airplane` não têm nada em comum na hierarquia, mas ambos podem `IFly`:

csharp

```csharp
public interface IFly
{
    void Fly();
}

public class Duck : Animal, IFly
{
    public void Fly() => Console.WriteLine("Batendo asas");
}

public class Airplane : IFly
{
    public void Fly() => Console.WriteLine("Ligando turbinas");
}
```

`Duck` já herda de `Animal` (abstract class) e ainda implementa `IFly` — isso não seria possível com duas classes base.

#### Onde isso aparece MUITO em backend real: injeção de dependência

Esse é o uso mais importante que você vai ver no dia a dia com ASP.NET Core:

csharp

```csharp
public interface IClientRepository
{
    Client GetById(int id);
    void Add(Client client);
}

public class ClientRepository : IClientRepository
{
    private readonly AppDbContext _context;

    public ClientRepository(AppDbContext context) => _context = context;

    public Client GetById(int id) => _context.Clients.Find(id);
    public void Add(Client client) => _context.Clients.Add(client);
}
```

csharp

```csharp
public class ClientService
{
    private readonly IClientRepository _repository; // depende da interface, não da classe concreta

    public ClientService(IClientRepository repository)
    {
        _repository = repository;
    }
}
```

E no `Program.cs` você registra qual implementação usar:

```csharp
builder.Services.AddScoped<IClientRepository, ClientRepository>();
```

**Por que isso importa:** `ClientService` nunca sabe que existe `ClientRepository` — ele só conhece `IClientRepository`. Isso permite trocar a implementação (ex: usar um `FakeClientRepository` em teste, sem tocar banco de verdade) sem mudar uma linha do `ClientService`. É a base de testabilidade e do princípio de inversão de dependência (o "D" do SOLID).

#### Interfaces prontas do próprio C# que você já usa sem perceber

- `IEnumerable<T>` — todo `List<T>`, `Array` implementa isso, é o que permite `foreach`
- `IDisposable` — o que o `using` chama por trás dos panos (`Dispose()`)
- `IComparable<T>` — permite `.Sort()` numa lista de objetos customizados