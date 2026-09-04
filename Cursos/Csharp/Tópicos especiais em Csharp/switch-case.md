Em C#, o `switch` avalia uma expressão e executa o bloco correspondente ao valor. Existem duas formas: a **tradicional (statement)** e a **switch expression** (a partir do C# 8), mais moderna e concisa.

### Switch tradicional (statement)

```csharp
int dia = 3;
string nome;

switch (dia)
{
    case 1:
        nome = "Segunda";
        break;
    case 2:
        nome = "Terça";
        break;
    case 3:
    case 4: // fall-through: agrupa múltiplos cases
        nome = "Meio de semana";
        break;
    default:
        nome = "Desconhecido";
        break;
}
```

- **Cada `case` precisa de `break`, `return`, `continue` ou `goto`** — C# não permite fall-through implícito (diferente de C/JS), exceto quando os cases estão vazios um em cima do outro (como `case 3:` e `case 4:` acima).
- `default` é opcional, mas boa prática incluir.

### Switch expression (moderno, C# 8+)

Mais enxuto, ideal quando cada case só retorna um valor:

```csharp
string nome = dia switch
{
    1 => "Segunda",
    2 => "Terça",
    3 or 4 => "Meio de semana",
    _ => "Desconhecido" // equivale ao default
};
```

### Pattern matching (bem útil, C# 7+)

O switch em C# também aceita padrões, não só valores fixos:

```csharp
object valor = 42;

string resultado = valor switch
{
    int n when n > 100 => "Número grande",
    int n => $"Número: {n}",
    string s => $"Texto: {s}",
    null => "Nulo",
    _ => "Tipo desconhecido"
};
```

Isso é bem comum em cenários de validação de DTOs ou tratamento de tipos polimórficos, por exemplo.