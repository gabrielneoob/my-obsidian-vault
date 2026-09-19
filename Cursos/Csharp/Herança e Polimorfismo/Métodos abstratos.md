- São métodos que não possuem implementação

- Métodos precisam ser abstratos quando a classe é genérica demais para conter sua implementação

- Se uma classe possuir pelo menos um métodos abstrato, então esta classe também é abstrata

- Notação UML: itálica


![[Pasted image 20260913165807.png]]

### `abstract` vs `virtual`

A diferença central: **`virtual` tem implementação padrão opcional pra sobrescrever; `abstract` não tem implementação nenhuma e obriga a sobrescrita.**

csharp

```csharp
public abstract class Animal
{
    // virtual: tem corpo, filha PODE sobrescrever, mas não é obrigada
    public virtual void MakeSound()
    {
        Console.WriteLine("Some generic sound...");
    }

    // abstract: sem corpo, filha É OBRIGADA a implementar
    public abstract void Move();
}

public class Dog : Animal
{
    public override void Move()
    {
        Console.WriteLine("Correndo com 4 patas");
    }

    // Não é obrigado a sobrescrever MakeSound() — se não fizer, usa o comportamento genérico
}

public class Snake : Animal
{
    public override void Move()
    {
        Console.WriteLine("Rastejando");
    }

    public override void MakeSound() // aqui sim decidiu sobrescrever
    {
        Console.WriteLine("Hiss...");
    }
}
```

||`virtual`|`abstract`|
|---|---|---|
|Tem corpo/implementação?|Sim|Não|
|Override é obrigatório?|Não, é opcional|Sim, obrigatório na primeira classe concreta|
|Pode existir numa classe não-abstrata?|Sim|Não — só dentro de `abstract class`|
|Uso típico|Comportamento padrão que às vezes muda|Comportamento que cada filha _precisa_ definir do seu jeito, sem padrão sensato|

**Regra prática pra decidir:** se existe um comportamento genérico razoável que serve pra maioria das filhas → `virtual`. Se não existe nenhum comportamento genérico que faça sentido (cada filha tem que resolver do seu jeito, sem exceção) → `abstract`.

No seu exemplo do `Person`/`Client`: `GetRole()` faz mais sentido como `abstract`, porque não existe um "papel genérico" sensato — cada tipo de pessoa (`Client`, `Employee`) precisa dizer o seu. Já algo como um método `Print()` que formata dados básicos poderia ser `virtual`, porque tem um comportamento padrão razoável que só às vezes precisa mudar.