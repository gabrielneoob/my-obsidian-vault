Em C#, `var` permite que o compilador infira o tipo da variável a partir do valor atribuído, em tempo de compilação. Não é tipagem dinâmica — o tipo é fixado na declaração e não pode mudar depois.

```csharp
var nome = "Gabriel";      // string
var idade = 30;            // int
var preco = 19.99m;        // decimal
var lista = new List<int>(); // List<int>

// isso dá erro, pois o tipo já foi fixado como string:
// nome = 10;
```

**Regras importantes:**

- Precisa ser inicializada na mesma linha da declaração (`var x;` sem valor não compila).
- O tipo é determinado em tempo de compilação, então não há perda de performance comparado a declarar o tipo explicitamente.
- Muito comum com LINQ, onde o tipo de retorno pode ser complexo ou anônimo:


```csharp
var resultado = lista.Where(x => x > 10).Select(x => x * 2);
// tipo real seria algo como IEnumerable<int>, mas var deixa mais limpo
```

**Quando usar (convenção comum):**

- Quando o tipo já é óbvio pelo lado direito (`var db = new AppDbContext();`)
- Com tipos anônimos (`var obj = new { Nome = "x", Idade = 1 };`) — aqui é obrigatório, pois não existe outro jeito de nomear o tipo.
- Com LINQ e generics longos, para reduzir verbosidade.

**Quando evitar:**

- Quando o tipo não fica claro pelo contexto (ex: `var resultado = Calcular();` — não dá pra saber se é `int`, `decimal`, etc. sem olhar a assinatura do método).