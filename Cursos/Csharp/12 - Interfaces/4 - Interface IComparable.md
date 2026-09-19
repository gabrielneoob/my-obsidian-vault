### `IComparable<T>` em C#

Interface que permite definir **como dois objetos do seu tipo devem ser comparados** — é o que possibilita usar `.Sort()`, `Array.Sort()`, `OrderBy` etc. em listas de objetos customizados.

#### Contrato da interface

csharp

```csharp
public interface IComparable<T>
{
    int CompareTo(T other);
}
```

`CompareTo` retorna:

- **Negativo** → objeto atual vem _antes_ de `other`
- **Zero** → são iguais (pra fins de ordenação)
- **Positivo** → objeto atual vem _depois_ de `other`

#### Implementando no seu domínio

csharp

```csharp
public class Client : IComparable<Client>
{
    public string Name { get; set; }
    public DateOnly BirthDate { get; set; }

    public int CompareTo(Client other)
    {
        return Name.CompareTo(other.Name); // ordena por nome, alfabético
    }
}
```

Com isso, uma `List<Client>` já sabe se ordenar sozinha:


```csharp
List<Client> clients = new List<Client>();
clients.Add(new Client { Name = "Carlos", ... });
clients.Add(new Client { Name = "Ana", ... });

clients.Sort(); // usa o CompareTo automaticamente
```

#### Comparando por outro critério (ex: idade em vez de nome)

Se o critério "natural" de ordenação é `Name`, mas às vezes você precisa ordenar por `BirthDate`, você não muda o `CompareTo` — usa LINQ com uma lambda em vez de depender do `IComparable`:

csharp

```csharp
var ordenadoPorIdade = clients.OrderBy(c => c.BirthDate).ToList();
```

`IComparable` define a ordenação _padrão/natural_ do tipo; pra critérios alternativos, `OrderBy`/`IComparer<T>` são a ferramenta certa (isso é além do escopo de agora, mas vale saber que existe pra não achar que `IComparable` é a única forma de ordenar).

#### Por que `CompareTo` em vez de subtrair direto

Cuidado com essa armadilha comum:

csharp

```csharp
// ERRADO em geral (funciona só às vezes, por acaso)
public int CompareTo(Client other) => BirthDate.Year - other.BirthDate.Year;

// CORRETO
public int CompareTo(Client other) => BirthDate.CompareTo(other.BirthDate);
```

Subtração direta pode estourar overflow com `int` grande, ou dar resultado errado com `double`/`float` (por causa de arredondamento). `DateOnly`, `int`, `string`, praticamente todo tipo básico do C# já implementa `IComparable` — então o padrão é sempre delegar pro `CompareTo` do campo, não reinventar a lógica de comparação na mão.

#### Ligação com o que já vimos

`IComparable<T>` é o mesmo padrão de interface que `IShape`/`IDiscountable`: um contrato que qualquer classe pode implementar, sem precisar de herança — só que esse aqui já vem pronto no .NET e é reconhecido nativamente por `Sort()`, `Array.Sort()`, `List<T>.BinarySearch()`, etc.

**Exercício pra fixar:** implemente `IComparable<Product>` em `Product`, comparando por `Price`. Depois crie uma `List<Product>` com uns 4 produtos fora de ordem, chame `.Sort()` e imprima pra ver ordenando do mais barato pro mais caro.