- É um recurso do C# para que dados de tipo valor (structs) possam receber o valor null

- Uso comun:
	- Campos de banco de dados que podem valer nulo (data de nascimento, algum valor numérico, etc.).
	- Dados e parâmetros opcionais

**Nullable em C#**

- É um recurso do C# que permite que tipos valor (`struct`, como `int`, `double`, `bool`, `DateTime`) recebam o valor `null`, algo que normalmente só é possível com tipos referência (`class`).
- Por baixo dos panos, `Nullable<T>` é uma struct genérica (`System.Nullable<T>`) que "embrulha" o tipo original e adiciona a informação de se há ou não um valor.

**Sintaxes equivalentes:**

csharp

```csharp
Nullable<double> x = null;
double? x = null; // forma abreviada, mais usada na prática
```

**Usos comuns:**

- Campos de banco de dados que podem ser nulos (data de nascimento, um valor numérico opcional, etc.)
- Parâmetros e dados opcionais em métodos/DTOs
- Representar "ausência de valor" de forma explícita (diferente de usar um valor "mágico" tipo `-1` ou `0`)

**Membros úteis do `Nullable<T>`:**

```csharp
double? x = null;

x.HasValue      // bool: indica se tem valor (false aqui)
x.Value         // lança InvalidOperationException se HasValue for false
x ?? 0.0        // operador de coalescência nula: retorna 0.0 se x for null
x?.ToString()   // null-conditional operator, evita NullReferenceException
```

**Exemplo prático:**

```csharp
double? valor = ObterValorDoBanco();

if (valor.HasValue)
{
    Console.WriteLine($"Valor: {valor.Value}");
}
else
{
    Console.WriteLine("Sem valor definido.");
}

// forma mais concisa
Console.WriteLine($"Valor: {valor ?? 0}");
```

- Métodos:
	- GetValueOrDefault
	- HasValue
	- Value(lança uma exceção se não houver valor)

- Um nullable não pode ser atribuído para um struct comum
```c#
namespace Course
{
    class Program
    {
        static public void Main()
        {
            Nullable<double> x = null;

            double? y = null;
            double? z = 10.0;

            Console.WriteLine(x.GetValueOrDefault());
            Console.WriteLine(z.GetValueOrDefault());

            Console.WriteLine(x.HasValue);
            Console.WriteLine(z.HasValue);

            if(x.HasValue)
                Console.WriteLine(x.Value);
            else
                Console.WriteLine("X is null");


            if (z.HasValue)
                Console.WriteLine(z.Value);
            else
                Console.WriteLine("Z is null");
        }
    }
}
```