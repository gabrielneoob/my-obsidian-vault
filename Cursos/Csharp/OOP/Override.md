### O que está acontecendo

Toda classe em C# herda implicitamente de `object`, que já define um método `ToString()` padrão. Esse método padrão simplesmente retorna o nome completo do tipo (ex: `"MeuNamespace.Produto"`), o que geralmente não é muito útil.

Quando você escreve:

```csharp
public override string ToString()
{
    return nome + ", $ " + preco.ToString("F2", CultureInfo.InvariantCulture);
}
```

Você está dizendo: "para esta classe específica, quero que `ToString()` se comporte de forma diferente do padrão herdado de `object`". Ou seja, você está substituindo a implementação original por uma sua.

### Por que precisa da palavra-chave `override`

Em C#, você não pode simplesmente redefinir um método herdado sem avisar o compilador da sua intenção. A palavra `override` serve para:

1. **Indicar intenção explícita** — deixa claro que você sabe que está substituindo algo, e não criando um método novo por acidente.
2. **Habilitar polimorfismo** — graças a isso, se você tiver `object obj = new Produto();` e chamar `obj.ToString()`, o C# vai chamar a versão sobrescrita (a sua), não a do `object`. Isso só funciona porque `ToString()` na classe `object` é marcado como `virtual` (pode ser sobrescrito).
3. **Segurança em tempo de compilação** — se você tentasse usar `override` em um método que não é `virtual`/`abstract` na base, o compilador daria erro. Isso evita bugs sutis.

### Na prática, no seu exemplo

Sempre que alguém fizer:

csharp

```csharp
Console.WriteLine(meuProduto);
// ou
string texto = meuProduto.ToString();
```

O C# vai chamar automaticamente essa versão customizada, retornando algo como `"Camiseta, $ 49.90"` em vez do nome genérico do tipo. Isso é super comum para depuração, logs e exibição amigável de objetos.