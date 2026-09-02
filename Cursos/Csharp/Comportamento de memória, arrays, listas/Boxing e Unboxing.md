Boxing e unboxing são sobre como o C# lida com **tipos de valor** (`value types`) versus **tipos de referência** (`reference types`) na memória.

### O conceito base

- **Tipos de valor** (`int`, `double`, `bool`, `struct`, etc.) ficam na **stack** — são armazenados diretamente.
- **Tipos de referência** (`class`, `string`, `object`, arrays) ficam no **heap** — a variável guarda um "endereço" que aponta pra lá.

### Boxing — converter valor em referência

Quando você pega um tipo de valor e "empacota" ele como `object`, o C# precisa copiá-lo pro heap:

csharp

```csharp
int numero = 42;        // stack
object caixa = numero;  // BOXING: copia o valor pro heap, "caixa" aponta pra lá
```

Isso acontece silenciosamente sempre que você atribui um tipo de valor a algo do tipo `object` (ou a uma interface que ele implementa).

### Unboxing — converter de volta

csharp

```csharp
object caixa = 42;
int numero = (int)caixa; // UNBOXING: precisa de cast explícito
```

Unboxing sempre exige cast explícito, e se o tipo não bater, lança `InvalidCastException`.

### Por que isso importa na prática

**Custo de performance.** Cada boxing cria um objeto novo no heap — isso significa alocação de memória e, eventualmente, trabalho pro garbage collector. Se isso acontece dentro de um loop grande, o impacto é real:

csharp

```csharp
ArrayList lista = new ArrayList(); // tipo antigo, guarda tudo como object

for (int i = 0; i < 1_000_000; i++)
{
    lista.Add(i); // BOXING em cada iteração — 1 milhão de alocações no heap!
}
```

### Onde isso conecta com banco de dados / mercado

**1. Motivo real de existir `List<T>` genérico em vez de `ArrayList`:**

csharp

```csharp
// Jeito antigo (evita, mas você pode encontrar em código legado)
ArrayList numeros = new ArrayList();
numeros.Add(10); // boxing

// Jeito moderno — sem boxing, porque List<T> é tipado
List<int> numeros = new List<int>();
numeros.Add(10); // sem boxing, int fica direto na lista
```

Isso é literalmente **por que genéricos (`<T>`) existem** em C# — pra evitar boxing/unboxing desnecessário. É uma pergunta clássica de entrevista: _"por que usar `List<int>` em vez de `ArrayList`?"_

**2. `DataRow` / `DataTable` (ADO.NET clássico, ainda aparece em sistemas legados de banco):**

csharp

```csharp
DataRow row = dataTable.Rows[0];
int id = (int)row["Id"]; // unboxing — row["Id"] retorna object
```

Se você trabalhar com sistema legado que usa `ADO.NET` puro (sem EF Core), boxing/unboxing aparece toda hora, porque `DataRow` guarda tudo como `object`.

**3. Reflection e serialização genérica:**

Bibliotecas de mapeamento objeto-relacional por baixo dos panos fazem boxing quando lidam com tipos desconhecidos em tempo de compilação (via `object`), embora EF Core moderno seja bem otimizado nisso.

### Resumindo pro mercado

- No dia a dia com **EF Core + LINQ tipado**, você quase nunca vai escrever boxing manualmente — o próprio uso de genéricos (`List<T>`, `DbSet<T>`) já evita isso por design.
- Mas é **pergunta clássica de entrevista teórica**: _"o que é boxing/unboxing e por que genéricos evitam isso?"_ — vale saber explicar de cabeça.
- Se você mexer em código legado com `ArrayList` ou `ADO.NET` puro, vai ver bastante boxing/unboxing na prática.