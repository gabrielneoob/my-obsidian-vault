- Representa uma DURAÇÃO
- É um tipo valor (struct)

- Um objeto TimeSpan internamente armazena uma duração na forma de ticks(100 nanosegundos)

```c#
TimeSpan t1 = new TimeSpan(0, 1, 30);
Console.WriteLine(t1);
Console.WriteLine(t1.Ticks);
```

`TimeSpan` representa um **intervalo de tempo** (duração), diferente de `DateTime`, que representa um **ponto no tempo**. Pense assim: `DateTime` é "2 de setembro de 2026, 14:30", enquanto `TimeSpan` é "1 hora e 30 minutos".

### O exemplo

```csharp
TimeSpan t1 = new TimeSpan(0, 1, 30); // 0 horas, 1 minuto, 30 segundos
Console.WriteLine(t1);        // 00:01:30
Console.WriteLine(t1.Ticks);  // 900000000
```

- **Saída do `WriteLine(t1)`**: `00:01:30` (formato padrão `hh:mm:ss`)
- **Ticks**: 1 tick = 100 nanossegundos. Como 1 segundo = 10.000.000 ticks, 90 segundos (1min30s) = **900.000.000 ticks**.

Esse construtor `new TimeSpan(horas, minutos, segundos)` é um dos vários overloads — também existem `TimeSpan(dias, horas, min, seg)` e `TimeSpan(dias, horas, min, seg, ms)`.

### Para que serve, na prática

Sim, é bastante usado. Alguns cenários comuns no dia a dia de backend (tipo o que você trabalha):

**1. Diferença entre datas/horas**

```csharp
DateTime inicio = new DateTime(2026, 9, 2, 10, 0, 0);
DateTime fim = new DateTime(2026, 9, 2, 14, 30, 0);
TimeSpan duracao = fim - inicio; // subtração de DateTime retorna TimeSpan
Console.WriteLine(duracao); // 04:30:00
```

**2. Timeout / configuração de tempo de expiração**

```csharp
var options = new DistributedCacheEntryOptions
{
    AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(10)
};
```

Muito comum em cache (Redis), configuração de `HttpClient.Timeout`, JWT expiration, etc.

**3. Medir tempo de execução**

```csharp
var sw = Stopwatch.StartNew();
// ... código
sw.Stop();
Console.WriteLine(sw.Elapsed); // retorna um TimeSpan
```

**4. Delays/agendamento**

```csharp
await Task.Delay(TimeSpan.FromSeconds(5));
```

### Métodos estáticos úteis (bem mais usados que o construtor direto)

```csharp
TimeSpan.FromSeconds(90);
TimeSpan.FromMinutes(1.5);
TimeSpan.FromHours(2);
TimeSpan.FromDays(1);
```

Na prática, `TimeSpan.FromX(...)` é usado com muito mais frequência do que o construtor `new TimeSpan(h, m, s)` — principalmente em configs de timeout, cache e agendamento, que é algo que provavelmente já apareceu no seu trabalho com AWS/Docker (tipo configurar timeout de request ou TTL de cache).

## Propriedades e Operações

```c#
namespace Course
{
    class Program
    {
        static public void Main()
        {

            TimeSpan t1 = new TimeSpan(1, 30, 10);
            TimeSpan t2 = new TimeSpan(0, 10, 5);

            TimeSpan sum = t1.Add(t2);
            TimeSpan dif = t1.Subtract(t2);

            Console.WriteLine(sum);
            Console.WriteLine(dif);
        }
    }
}
```