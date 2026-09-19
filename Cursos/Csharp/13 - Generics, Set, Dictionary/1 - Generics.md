- Generics permitem que classes, interfaces e métodos possam ser parametizados por tipo. Seus benefícios são
	- Reuso
	- Type safety
	- Performance

- Uso comum: coleções

```c#
List<string> list = new list<string>();

list.Add("Maria");
string name = list[0];

```

### Generics em C#

Generics permitem escrever código que funciona com **qualquer tipo**, definido só na hora do uso — sem duplicar lógica pra cada tipo diferente e sem perder verificação de tipo em tempo de compilação.

#### O problema que resolve

Sem generics, você teria que duplicar código pra cada tipo:

csharp

```csharp
public class IntStack
{
    public void Push(int item) { ... }
    public int Pop() { ... }
}

public class StringStack
{
    public void Push(string item) { ... }
    public string Pop() { ... }
}
```

Ou usar `object`, perdendo tipagem (e precisando de cast, com risco de erro em runtime):

csharp

```csharp
public class ObjectStack
{
    public void Push(object item) { ... }
    public object Pop() { ... }
}

var stack = new ObjectStack();
stack.Push(5);
string s = (string)stack.Pop(); // compila, mas explode em runtime
```

#### Com generics

csharp

```csharp
public class Stack<T>
{
    private List<T> _items = new List<T>();

    public void Push(T item) => _items.Add(item);
    public T Pop()
    {
        T last = _items[^1];
        _items.RemoveAt(_items.Count - 1);
        return last;
    }
}
```

csharp

```csharp
var intStack = new Stack<int>();
intStack.Push(5);
int x = intStack.Pop(); // sem cast, tipado, erro pego em compilação

var clientStack = new Stack<Client>();
clientStack.Push(new Client("Gabriel", "email@x.com", birthDate));
```

`T` é um **placeholder de tipo** — só é resolvido quando você usa a classe (`Stack<int>`, `Stack<Client>`).

#### Generics em método (não precisa ser a classe toda genérica)

csharp

```csharp
public T FindMax<T>(List<T> items) where T : IComparable<T>
{
    T max = items[0];
    foreach (var item in items)
    {
        if (item.CompareTo(max) > 0)
            max = item;
    }
    return max;
}
```

Aqui liga direto com o que você acabou de ver: `where T : IComparable<T>` é uma **constraint** (restrição) — diz "esse método só aceita tipos que implementam `IComparable<T>`", porque é isso que permite chamar `.CompareTo()` dentro do método. Sem essa constraint, o compilador nem deixaria compilar (`T` genérico puro não tem `CompareTo`).

#### Constraints mais comuns

csharp

```csharp
where T : class          // só tipo referência
where T : struct         // só tipo valor
where T : new()           // precisa ter construtor sem parâmetros
where T : IComparable<T>  // precisa implementar essa interface
where T : Person          // precisa herdar de Person (ou ser Person)
```

#### Onde você já usa generics sem perceber

Isso é o ponto mais importante pra fixar: você usa generics **o tempo todo** desde o começo do curso, só não tinha nome ainda:

csharp

```csharp
List<OrderItem> items = new List<OrderItem>();  // List<T>
List<IShape> shapes = new List<IShape>();
Dictionary<string, int> counts = new Dictionary<string, int>(); // dois parâmetros de tipo
```

`List<T>` é uma classe genérica do próprio .NET — funciona pra qualquer tipo, tipada, sem cast. É exatamente o padrão do `Stack<T>` que construímos acima.

#### Ligando com o repositório que vimos antes

csharp

```csharp
public interface IRepository<T>
{
    void Add(T item);
    List<T> GetAll();
}

public class Repository<T> : IRepository<T>
{
    private List<T> _items = new List<T>();
    public void Add(T item) => _items.Add(item);
    public List<T> GetAll() => _items;
}
```

Com isso, uma única classe serve pra `Repository<Client>`, `Repository<Product>`, `Repository<Order>` — sem reescrever `ClientRepository`, `ProductRepository` cada um do zero. É o padrão real usado em Entity Framework Core (`DbSet<T>` é exatamente isso).

**Exercício pra fixar:** crie uma classe genérica `Pair<T>` com duas propriedades `First` e `Second` do tipo `T`, e um método `Swap()` que troca os valores. Depois teste com `Pair<int>` e `Pair<string>`.