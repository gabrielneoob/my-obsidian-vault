```c#
namespace Course
{
    internal class Calculadora
    {
        // Com sobrecargas
        //public static int Sum(int n1, int n2)
        //{
        //    return n1 + n2;
        //}

        //public static int Sum(int n1, int n2, int n3)
        //{
        //    return n1 + n2 + n3;
        //}

        //public static int Sum(int n1, int n2, int n3, int n4)
        //{
        //    return n1 + n2 + n3 + n4;
        //}

        // Com vetor
        //public static int Sum(int[] numbers)
        //{
        //    int sum = 0;

        //    for (int i = 0; i < numbers.Length; i++)
        //    {
        //        sum += numbers[i];
        //    }

        //    return sum;
        //}

        // Usando params
        public static int Sum(params int[] numbers)
        {
            int sum = 0;

            for (int i = 0; i < numbers.Length; i++)
            {
                sum += numbers[i];
            }

            return sum;
        }
    }
}
```

```c#

namespace Course
{
    class Program
    {
        static public void Main()
        {
            //int s1 = Calculadora.Sum(new int[] {10, 20, 30, 40});

            // Usando params
            int s1 = Calculadora.Sum(2,4,3);
        }
  
    }
}
```

### Regra técnica importante do `out`

O método é **obrigado** a atribuir um valor ao parâmetro `out` antes de retornar — o compilador não deixa compilar se você esquecer. Isso é diferente do `ref`, onde o valor já vem inicializado de fora e o método pode ou não alterar.

### Resumindo o motivo de valer a pena entender

Você vai encontrar `out` toda vez que precisar de **"tentar fazer algo que pode falhar, sem lançar exceção"**: parse de números, parse de datas (`DateTime.TryParse`), parse de enums (`Enum.TryParse`), busca em dicionário, conversões de tipo... É um padrão recorrente, não um recurso isolado.

### O que é

`out` é um modificador de parâmetro que permite um método **retornar um valor extra** através de um dos seus parâmetros, além do `return` normal.

### Por que existe

Um método normalmente só retorna **uma coisa** (via `return`). Mas às vezes você precisa que ele devolva **duas informações ao mesmo tempo** — por exemplo: "deu certo?" (bool) e "qual foi o resultado?" (o valor em si).

```csharp
bool sucesso = int.TryParse("123", out int numero);
```

Aqui, `TryParse` te devolve **duas coisas**:

- `sucesso` → via `return` normal (`true`/`false`)
- `numero` → via `out`, o valor convertido

### Como funciona por dentro

O parâmetro marcado com `out` não é uma cópia — é uma **referência direta à variável de fora**. Quando o método escreve dentro dele, está escrevendo direto na variável que você declarou na chamada.


```csharp
static void Dobrar(out int resultado)
{
    resultado = 10; // escreve direto na variável de fora
}

Dobrar(out int x);
Console.WriteLine(x); // 10
```

### As 3 regras do `out`

1. **A variável não precisa estar inicializada antes de passar** (diferente de `ref`, que exige valor prévio):


```csharp
int x; // pode ficar "vazia"
Dobrar(out x);
```

2. **O método é obrigado a atribuir um valor antes de terminar** — o compilador força isso, senão dá erro de compilação.
3. **Você pode declarar a variável direto na chamada** (jeito moderno, C# 7+):


```csharp
Dobrar(out int x); // declara "x" ali mesmo
```

### Onde você mais vai ver

Sempre em métodos que "tentam" fazer algo e podem falhar, sem lançar exceção — daí o prefixo `Try`:

csharp

```csharp
int.TryParse(texto, out int numero)
DateTime.TryParse(texto, out DateTime data)
dicionario.TryGetValue(chave, out int valor)
Enum.TryParse(texto, out MeuEnum valor)
```

### Resumo em uma frase

`out` é como se o método tivesse "duas portas de saída" — o `return` de sempre, e um valor extra que ele injeta direto na sua variável.