### HashSet

Ambos são coleções que **não permitem duplicatas** — a diferença central é se mantêm ordem ou não.

### HashSet— unicidade, sem ordem garantida

csharp

```csharp
var emails = new HashSet<string>();
emails.Add("gabriel@x.com");
emails.Add("gabriel@x.com"); // ignorado, já existe
emails.Add("outro@x.com");

Console.WriteLine(emails.Count); // 2
```

- Usa **hash table** por baixo — é exatamente onde `GetHashCode`/`Equals` entram em ação (ligando direto com o que vimos antes).
- Buscar, adicionar, remover: **O(1)** em média — muito mais rápido que procurar numa `List<T>` (`Contains` numa lista é O(n)).
- **Não garante ordem** de iteração — pode sair em qualquer sequência.

csharp

```csharp
var clientes = new HashSet<Client>(); // precisa de Equals/GetHashCode sobrescritos
clientes.Add(new Client { Email = "gabriel@x.com" });
clientes.Add(new Client { Email = "gabriel@x.com" }); // ignorado, mesmo Email
```

#### SortedSet — unicidade, com ordem automática

csharp

```csharp
var numeros = new SortedSet<int> { 5, 1, 3, 1, 4 };
foreach (var n in numeros)
    Console.WriteLine(n);
// Saída: 1, 3, 4, 5 — duplicata removida E ordenado automaticamente
```

- Mantém os elementos **sempre ordenados** (implementado como árvore balanceada por trás).
- Exige que `T` implemente `IComparable<T>` (ou você passe um `IComparer<T>` customizado no construtor) — **aqui sim** é onde o `CompareTo` que implementamos antes entra em uso direto:

csharp

```csharp
var clientesOrdenados = new SortedSet<Client>(); // Client precisa implementar IComparable<Client>
clientesOrdenados.Add(new Client { Email = "carlos@x.com" });
clientesOrdenados.Add(new Client { Email = "ana@x.com" });
// itera automaticamente: ana primeiro, depois carlos
```

- Operações: **O(log n)** — mais lento que `HashSet` (que é O(1)), porque manter ordenado tem custo.

#### Quando usar cada um

||`HashSet<T>`|`SortedSet<T>`|
|---|---|---|
|Precisa de ordem?|Não|Sim|
|Prioridade|Velocidade máxima|Ordem + unicidade|
|Depende de|`Equals`/`GetHashCode`|`IComparable<T>`|
|Performance|O(1)|O(log n)|

#### Casos reais

- **`HashSet<string>`** — checar rapidamente se um valor já foi processado (ex: emails já enviados numa campanha, IDs já visitados num algoritmo).
- **`HashSet<int>`** — interseção/união/diferença de conjuntos (`.IntersectWith()`, `.UnionWith()`, `.ExceptWith()` — métodos nativos pra operações de conjunto matemático).
- **`SortedSet<T>`** — ranking (top N sempre ordenado conforme insere), leaderboard, ou qualquer caso onde você precisa de unicidade **e** iterar sempre em ordem sem chamar `.Sort()` toda hora.

Em backend real com banco de dados, esses dois aparecem menos que `List<T>`/LINQ (porque ordenação e distinct geralmente ficam no `ORDER BY`/`DISTINCT` do SQL), mas são úteis pra processamento em memória — cache, deduplicação de dados vindos de múltiplas fontes, algoritmos que rodam depois que os dados já foram carregados do banco.

Isso, você fechou o resumo certinho. Só um ajuste fino no `HashSet`:

> `SortedSet<T>` mantém ordem, dependendo de `IComparable<T>` — certo, exatamente isso.
> 
> `HashSet<T>` não é "só" pra impedir duplicatas — impedir duplicata é a **consequência**, não o objetivo principal. O objetivo central é **busca/inserção rápida (O(1))**, usando `GetHashCode`/`Equals` como mecanismo pra saber "isso já existe aqui?" de forma eficiente. A ausência de duplicatas é um efeito colateral de como a estrutura funciona por dentro (não consegue inserir duas vezes no mesmo "balde" sem ela perceber que já tem algo igual lá).

Reformulando sua frase com esse ajuste:

 `HashSet<T>` garante unicidade e permite verificação rápida (O(1)) se um item já existe, usando `Equals`/`GetHashCode` por trás. `SortedSet<T>` também garante unicidade, mas além disso mantém os itens sempre ordenados, usando `IComparable<T>` (ou um `IComparer<T>` customizado) pra decidir a ordem.

A diferença prática que resume tudo: se você só precisa saber "isso já existe?" o mais rápido possível e não liga pra ordem → `HashSet`. Se você precisa que a coleção **sempre** saia ordenada quando você iterar, e aceita pagar um pouco mais de custo (O(log n) em vez de O(1)) por isso → `SortedSet`.