### GetHashCode e Equals

Duas operações herdadas de `object`, usadas para **comparar se um objeto é igual a outro**.

#### Equals

Faz a comparação completa e definitiva: compara os valores relevantes do objeto e diz com certeza se dois objetos são iguais ou não.

csharp

```csharp
public override bool Equals(object obj)
{
    if (obj is not Client other) return false;
    return Email == other.Email;
}
```

#### GetHashCode

Retorna um número (hash) que representa o objeto — usado como "endereço rápido" para localizar o objeto em coleções como `HashSet` e `Dictionary`.

csharp

```csharp
public override int GetHashCode()
{
    return Email.GetHashCode();
}
```

#### O contrato entre os dois

> Se `Equals` retorna `true` para dois objetos → eles **obrigatoriamente** têm o mesmo `GetHashCode()`.  
> Mas dois objetos com o mesmo hash não são necessariamente iguais (pode haver colisão).

Se você sobrescreve um sem sobrescrever o outro de forma consistente, a classe quebra silenciosamente dentro de `HashSet`/`Dictionary`.

#### Por que hash existe (não é sobre "menos confiável")

Em coleções baseadas em hash, o processo é:

1. Calcula `GetHashCode()` para saber em qual **bucket** procurar — rápido, O(1)
2. Se houver mais de um item no mesmo bucket, chama `Equals()` para confirmar igualdade real

Isso evita comparar o objeto com todos os outros da coleção um por um — sem hash, buscar em uma coleção grande seria O(n); com hash bem distribuído, é praticamente O(1).

#### Por que sobrescrever é necessário

Sem sobrescrever, `Equals` herdado de `object` compara **referência** (mesmo endereço de memória), não valor:

csharp

```csharp
var c1 = new Client { Name = "Gabriel" };
var c2 = new Client { Name = "Gabriel" };

c1.Equals(c2); // false — objetos diferentes na memória, mesmo com dados iguais
```

Tipos pré-definidos como `string` já sobrescrevem isso pra comparar valor:

csharp

```csharp
"teste".Equals("teste"); // true
```

#### Alternativa moderna: `record`

csharp

```csharp
public record Client(string Name, string Email);

var c1 = new Client("Gabriel", "email@x.com");
var c2 = new Client("Gabriel", "email@x.com");
c1.Equals(c2); // true, automático — record já gera Equals/GetHashCode por valor
```


### Exemplos práticos de GetHashCode e Equals

#### 1. Sem sobrescrever — bug clássico de duplicata "invisível"


```csharp
public class Product
{
    public string Name { get; set; }
    public double Price { get; set; }
}

var set = new HashSet<Product>();
set.Add(new Product { Name = "Mouse", Price = 50 });
set.Add(new Product { Name = "Mouse", Price = 50 }); // "duplicado" pra você

Console.WriteLine(set.Count); // 2 — HashSet não sabe que são "iguais"
```

Como `Equals`/`GetHashCode` não foram sobrescritos, o `HashSet` compara por referência de memória — são dois objetos diferentes, mesmo com dados idênticos.

#### 2. Sobrescrevendo — dedup funcionando de verdade

csharp

```csharp
public class Product
{
    public string Name { get; set; }
    public double Price { get; set; }

    public override bool Equals(object obj)
    {
        if (obj is not Product other) return false;
        return Name == other.Name && Price == other.Price;
    }

    public override int GetHashCode()
    {
        return HashCode.Combine(Name, Price); // helper do .NET pra combinar campos
    }
}
```

csharp

```csharp
var set = new HashSet<Product>();
set.Add(new Product { Name = "Mouse", Price = 50 });
set.Add(new Product { Name = "Mouse", Price = 50 });

Console.WriteLine(set.Count); // 1 — agora reconhece como igual
```

`HashCode.Combine(...)` é o jeito moderno recomendado de gerar hash a partir de múltiplos campos, em vez de escrever a fórmula de combinação na mão.

#### 3. Usando objeto customizado como chave de `Dictionary`

csharp

```csharp
public class Client
{
    public string Email { get; set; }

    public override bool Equals(object obj)
    {
        if (obj is not Client other) return false;
        return Email == other.Email;
    }

    public override int GetHashCode() => Email.GetHashCode();
}
```

csharp

```csharp
var descontosPorCliente = new Dictionary<Client, double>();

var c1 = new Client { Email = "gabriel@x.com" };
descontosPorCliente[c1] = 10.0;

var c2 = new Client { Email = "gabriel@x.com" }; // objeto diferente, mesmo email
Console.WriteLine(descontosPorCliente.ContainsKey(c2)); // true — sem sobrescrever, seria false
```

Isso é o cenário real onde isso mais aparece: usar um objeto de domínio (não só `string`/`int`) como chave em `Dictionary` ou item em `HashSet`, e precisar que "igual por valor" funcione.

#### 4. Comparando com `record` (sem escrever nada)

csharp

```csharp
public record Product(string Name, double Price);

var p1 = new Product("Mouse", 50);
var p2 = new Product("Mouse", 50);

Console.WriteLine(p1 == p2);        // true
Console.WriteLine(p1.Equals(p2));   // true
Console.WriteLine(p1.GetHashCode() == p2.GetHashCode()); // true
```

`record` gera `Equals`/`GetHashCode`/`==` automaticamente comparando **todos os campos por valor** — é a solução moderna pra não escrever esse boilerplate à mão sempre que precisar de comparação por valor.

#### Regra prática de quando sobrescrever manualmente vs usar `record`

- **Classe simples, imutável, só representa dados (DTO, Value Object)** → use `record`, ganha tudo de graça.
- **Entidade com identidade própria (ex: `Client` com um `Id` que nunca muda, mesmo se `Name`/`Email` mudarem)** → sobrescreva manualmente comparando só pelo `Id`, porque nesse caso "igual" significa "é a mesma entidade", não "tem os mesmos dados" — `record` compararia todos os campos, o que geralmente não é o que você quer pra entidade com identidade.