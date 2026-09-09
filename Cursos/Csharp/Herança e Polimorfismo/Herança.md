Herança é um dos pilares da orientação a objetos: permite que uma classe (derivada/filha) reaproveite membros de outra classe (base/pai), evitando duplicação de código.

### Sintaxe básica

csharp

```csharp
public class Animal
{
    public string Nome { get; set; }

    public Animal(string nome)
    {
        Nome = nome;
    }

    public void Comer()
    {
        Console.WriteLine($"{Nome} está comendo.");
    }

    public virtual void EmitirSom()
    {
        Console.WriteLine($"{Nome} faz um som genérico.");
    }
}

public class Cachorro : Animal
{
    public Cachorro(string nome) : base(nome) { }

    public override void EmitirSom()
    {
        Console.WriteLine($"{Nome} late: Au au!");
    }
}
```

Pontos-chave:

- `: Animal` na declaração da classe indica herança.
- `: base(nome)` chama o construtor da classe pai.
- `virtual` na classe base permite que o método seja sobrescrito.
- `override` na classe filha sobrescreve o comportamento.

### Regras importantes do C#

1. **Herança simples**: uma classe só pode herdar de **uma** classe base (diferente de interfaces, onde pode implementar várias).
2. **`sealed`**: impede que uma classe seja herdada.

csharp

```csharp
   public sealed class Gato : Animal { }
```

3. **`base`**: além do construtor, acessa membros da classe pai explicitamente (`base.EmitirSom()`).
4. **`protected`**: modificador de acesso visível para a classe e suas derivadas, mas não para o mundo externo.
5. **Classes abstratas**: quando você quer forçar as filhas a implementar um método, sem dar corpo na base.

csharp

```csharp
   public abstract class Forma
   {
       public abstract double CalcularArea();
   }

   public class Circulo : Forma
   {
       public double Raio { get; set; }
       public override double CalcularArea() => Math.PI * Raio * Raio;
   }
```

### Polimorfismo na prática

csharp

```csharp
Animal[] animais = { new Cachorro("Rex"), new Gato("Mimi") };

foreach (var a in animais)
{
    a.EmitirSom(); // chama a versão correta em runtime (polimorfismo)
}
```

Isso funciona por causa do `virtual`/`override` — o C# decide em tempo de execução qual método chamar, baseado no tipo real do objeto, não no tipo da variável.

---

### Exercício

Crie uma hierarquia `Funcionario` (base) → `Gerente` e `Desenvolvedor` (derivadas):

- `Funcionario` tem `Nome`, `SalarioBase` e um método virtual `CalcularSalario()` que retorna `SalarioBase`.
- `Gerente` sobrescreve `CalcularSalario()` somando um bônus fixo de R$2000.
- `Desenvolvedor` sobrescreve `CalcularSalario()` somando R$50 por cada certificação (`int QtdCertificacoes`).
- Crie uma lista de `Funcionario` com instâncias de ambos e imprima o salário calculado de cada um.