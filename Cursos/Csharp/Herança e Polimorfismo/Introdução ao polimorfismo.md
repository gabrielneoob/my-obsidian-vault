- Pilares da OOP
	- Encapsulamento
	- Herança
	- Polimorfismo

## Polimorfismo

Polimorfismo é a capacidade de objetos de tipos diferentes responderem à mesma "mensagem" (mesmo método/interface) de formas distintas, cada um com sua própria implementação.

Em Programação Orientada a Objetos(OOP), polimorfismo é recurso que permite que variáveis de um mesmo tipo mais genérico possam apontar para objetos de tipos específicos diferentes, tendo assim comportamentos diferentes conforme cada tipo específico

Polimorfismo é um dos quatro pilares da OOP (junto com encapsulamento, herança e abstração). A ideia central: **um mesmo método pode se comportar de forma diferente dependendo do objeto que o chama**.

O nome vem do grego — "muitas formas". Na prática, existem dois tipos principais:

### Polimorfismo de sobrescrita (runtime / dinâmico)

Uma classe base define um método, e as subclasses **sobrescrevem** esse comportamento. Em C#, isso usa `virtual` na base e `override` na subclasse.

```csharp
public class Animal
{
    public virtual string EmitirSom()
    {
        return "Som genérico de animal";
    }
}

public class Cachorro : Animal
{
    public override string EmitirSom()
    {
        return "Au au!";
    }
}

public class Gato : Animal
{
    public override string EmitirSom()
    {
        return "Miau!";
    }
}
```

O pulo do gato aqui:

```csharp
List<Animal> animais = new List<Animal> { new Cachorro(), new Gato(), new Animal() };

foreach (var animal in animais)
{
    Console.WriteLine(animal.EmitirSom());
}
// Au au!
// Miau!
// Som genérico de animal
```

Repare: a variável é do tipo `Animal`, mas o método que executa é o da classe **real** do objeto (`Cachorro`, `Gato`). Isso é resolvido em **tempo de execução** — daí "polimorfismo dinâmico".

### Polimorfismo de sobrecarga (compile-time / estático)

Você tem métodos com o **mesmo nome**, mas assinaturas diferentes (parâmetros diferentes). O compilador decide qual usar com base nos argumentos passados.

csharp

```csharp
public class Calculadora
{
    public int Somar(int a, int b) => a + b;
    public double Somar(double a, double b) => a + b;
    public int Somar(int a, int b, int c) => a + b + c;
}
```

Aqui a decisão é feita em **tempo de compilação** — daí "polimorfismo estático".

### Por que isso importa na prática

O maior ganho é escrever código genérico que trabalha com abstrações, sem precisar saber o tipo concreto:

csharp

```csharp
public interface IFormaGeometrica
{
    double CalcularArea();
}

public class Quadrado : IFormaGeometrica
{
    public double Lado { get; set; }
    public double CalcularArea() => Lado * Lado;
}

public class Circulo : IFormaGeometrica
{
    public double Raio { get; set; }
    public double CalcularArea() => Math.PI * Raio * Raio;
}

// Um método só, funciona pra qualquer forma:
public void ImprimirArea(IFormaGeometrica forma)
{
    Console.WriteLine($"Área: {forma.CalcularArea()}");
}
```

Isso é a base de praticamente todo design orientado a interfaces (repository pattern, strategy pattern, injeção de dependência) — você programa contra a abstração (`IFormaGeometrica`, `Animal`), e o comportamento certo aparece sozinho na hora de rodar, dependendo do que foi de fato instanciado.