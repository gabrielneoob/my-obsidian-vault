- São classes que não podem set instanciadas
- É uma forma de garantir herança total: somente subclasses não abstratas podem ser instanciadas, mas nunca a superclasse abstrata

**O que é:** uma classe que não pode ser instanciada diretamente — só serve como base para outras classes herdarem. Ela existe pra definir um contrato/comportamento comum, deixando parte da implementação para as classes filhas.

```csharp
public abstract class Shape
{
    public abstract double Area(); // sem corpo — cada filha implementa do seu jeito

    public void Print() // método concreto, herdado igual por todas
    {
        Console.WriteLine($"Área: {Area()}");
    }
}
```

**Regras principais:**

- `abstract class` não pode ser instanciada com `new Shape()` — só via classe derivada.
- Método `abstract` **não tem corpo** e obriga toda classe filha (não-abstrata) a implementá-lo com `override`.
- Pode misturar métodos abstratos com métodos concretos (com corpo) — diferente de interface, onde tradicionalmente tudo era sem implementação (hoje C# permite default implementation em interface também, mas a intenção é diferente).
- Pode ter campos, construtores e estado — interface não tem estado.

**Exemplo aplicando no seu domínio (Course.Entities):**

csharp

```csharp
public abstract class Person
{
    public string Name { get; set; }
    public string Email { get; set; }

    protected Person(string name, string email)
    {
        Name = name;
        Email = email;
    }

    public abstract string GetRole(); // cada tipo de pessoa define seu papel
}

public class Client : Person
{
    public DateOnly BirthDate { get; set; }

    public Client(string name, string email, DateOnly birthDate)
        : base(name, email)
    {
        BirthDate = birthDate;
    }

    public override string GetRole() => "Cliente";
}
```

Aqui `Person` nunca seria instanciada sozinha (não faz sentido "uma pessoa genérica" no seu domínio) — só faz sentido como `Client`, ou futuramente `Employee`, `Admin`, etc., cada um implementando `GetRole()` do seu jeito.

**Quando usar abstract class vs interface:** abstract class quando as classes filhas compartilham estado e implementação comum (como `Print()` no exemplo do `Shape`); interface quando você só quer garantir um contrato de comportamento sem impor uma hierarquia de herança (C# só permite herdar de uma classe, mas implementar várias interfaces).

- Polimorfismo: a superclasse classe genérica nos permite tratar de forma fácil e uniforme todos os tipos de conta, inclusive com polimorfismo se for o caso (como fizemos nos últimos exercícios). Por exemplo, você pode colocar todos tipos de contas em uma mesma coleção