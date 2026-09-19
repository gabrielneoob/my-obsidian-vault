### Tratamento de erros em C#

O mecanismo central é **try/catch/finally**, igual conceito de outras linguagens, mas com particularidades do C#.

#### Estrutura básica

```csharp
try
{
    int n = int.Parse("abc"); // vai estourar
}
catch (FormatException ex)
{
    Console.WriteLine($"Erro de formato: {ex.Message}");
}
finally
{
    Console.WriteLine("Sempre executa, com ou sem erro");
}
```

- `try` → onde o código arriscado roda
- `catch` → captura um tipo específico de exceção
- `finally` → roda sempre (útil pra fechar recursos, mas hoje em dia `using` substitui a maioria desses casos)

#### Múltiplos catches — do mais específico pro mais genérico

csharp

```csharp
try
{
    var order = ProcessOrder();
}
catch (FormatException ex)
{
    Console.WriteLine($"Formato inválido: {ex.Message}");
}
catch (DivideByZeroException ex)
{
    Console.WriteLine($"Divisão por zero: {ex.Message}");
}
catch (Exception ex) // genérico, sempre por último
{
    Console.WriteLine($"Erro inesperado: {ex.Message}");
}
```

A ordem importa: C# testa de cima pra baixo e usa o primeiro `catch` compatível. Se você colocar `catch (Exception)` primeiro, os outros nunca são alcançados (e o compilador acusa erro).

#### Exceções customizadas (muito usado em domínio de negócio)

```csharp
public class OrderException : Exception
{
    public OrderException(string message) : base(message) { }
}
```

```csharp
public class Order
{
    public void AddItem(OrderItem item)
    {
        if (item.Quantity <= 0)
            throw new OrderException("Quantidade deve ser maior que zero");

        Items.Add(item);
    }
}
```

Isso é o padrão pra erro de regra de negócio: você cria uma exceção com nome que já explica o problema, em vez de estourar `Exception` genérica.

#### No seu Program.cs — aplicando no lugar do crash que você teve


```csharp
try
{
    Console.Write("Birth Date: ");
    string birthDate = Console.ReadLine();

    DateOnly birthDateParsed = DateOnly.ParseExact(birthDate, "dd/MM/yyyy", CultureInfo.InvariantCulture);
    Client cl1 = new Client(name, email, birthDateParsed);

    // resto do processamento...
}
catch (FormatException)
{
    Console.WriteLine("Data em formato inválido. Use dd/MM/yyyy.");
}
catch (Exception ex)
{
    Console.WriteLine($"Erro inesperado: {ex.Message}");
}
```

Assim, em vez do `Unhandled exception` feio que você viu no terminal, o programa mostra uma mensagem legível e não crasha.

#### Padrão de backend (API) — diferente do console

Em API, você **não** espalha try/catch em todo controller. O padrão é um **middleware global de exceção**:

csharp

```csharp
public class ExceptionMiddleware
{
    private readonly RequestDelegate _next;

    public ExceptionMiddleware(RequestDelegate next) => _next = next;

    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await _next(context);
        }
        catch (OrderException ex)
        {
            context.Response.StatusCode = 400;
            await context.Response.WriteAsJsonAsync(new { error = ex.Message });
        }
        catch (Exception ex)
        {
            context.Response.StatusCode = 500;
            await context.Response.WriteAsJsonAsync(new { error = "Erro interno" });
        }
    }
}
```

Registrado uma vez no `Program.cs`/`Startup.cs`, isso captura qualquer exceção não tratada em qualquer request, sem precisar de try/catch repetido em cada endpoint — sua exceção customizada vira automaticamente um `400` com mensagem clara, e o resto vira `500` genérico (sem vazar detalhe interno pro cliente).

**Resumo da progressão:** `try/catch` local (o que você tá aprendendo agora) → exceções customizadas por domínio → middleware global centralizando tudo em backend real. É a mesma lógica em camadas cada vez mais amplas.