- É um tipo especial que serve para especificar de forma literal um conjunto de constantes relacionadas
- Palavra chave em C#: enum
	- Nota: enum é um tipo valor (struct)

- Vantagem: melhor semântica, código mais legível e auxiliado pelo compilador

`enum` (enumeração) é um tipo que representa um **conjunto fixo de valores nomeados**. Serve pra você substituir "números mágicos" ou strings soltas por nomes com significado, deixando o código mais legível e seguro.

### O problema que resolve

Sem `enum`, você pode acabar fazendo isso:

```csharp
int status = 1; // o que é "1"? Pendente? Aprovado? Cancelado?

if (status == 1)
{
    // ...
}
```

Isso é frágil — ninguém lembra o que cada número significa, e é fácil digitar o valor errado.

### Criando um enum

```csharp
public enum StatusPedido
{
    Pendente,   // 0
    Aprovado,   // 1
    Enviado,    // 2
    Cancelado   // 3
}
```

Por baixo dos panos, cada valor é um `int`, começando em `0` e incrementando — mas você usa pelo **nome**, não pelo número:

```csharp
StatusPedido status = StatusPedido.Aprovado;

if (status == StatusPedido.Aprovado)
{
    Console.WriteLine("Pedido aprovado!");
}
```

Muito mais legível e seguro — o compilador não deixa você atribuir qualquer coisa, só os valores válidos do enum.

### Definindo valores customizados

Você pode escolher os números manualmente (útil quando o valor precisa bater com algo específico, tipo um código de banco):

```csharp
public enum StatusPedido
{
    Pendente = 10,
    Aprovado = 20,
    Enviado = 30,
    Cancelado = 40
}
```

### Convertendo entre enum e outros tipos


```csharp
// Enum para int
int codigo = (int)StatusPedido.Aprovado; // 20

// int para enum
StatusPedido status = (StatusPedido)20; // StatusPedido.Aprovado

// Enum para string
string nome = StatusPedido.Aprovado.ToString(); // "Aprovado"

// String para enum (usando o TryParse que já vimos!)
if (Enum.TryParse("Aprovado", out StatusPedido resultado))
{
    Console.WriteLine(resultado); // Aprovado
}
```

Repare que `Enum.TryParse` segue exatamente o mesmo padrão do `out` que já explicamos — não é coincidência, é o mesmo idioma da linguagem se repetindo.

### Enum com `switch`


```csharp
string mensagem = status switch
{
    StatusPedido.Pendente => "Aguardando aprovação",
    StatusPedido.Aprovado => "Pedido aprovado",
    StatusPedido.Enviado => "A caminho",
    StatusPedido.Cancelado => "Pedido cancelado",
    _ => "Status desconhecido"
};
```

### Onde isso aparece no trabalho real com banco de dados

**1. Representando status/categorias no banco (muito comum):**

```csharp
public class Pedido
{
    public int Id { get; set; }
    public StatusPedido Status { get; set; }
}
```

O EF Core, por padrão, salva o enum como `int` no banco (o valor numérico). Mas você pode configurar pra salvar como `string`, o que é mais legível direto no banco:

```csharp
modelBuilder.Entity<Pedido>()
    .Property(p => p.Status)
    .HasConversion<string>(); // salva "Aprovado" em vez de 1
```

**2. Filtros em query:**

```csharp
var pedidosPendentes = await _context.Pedidos
    .Where(p => p.Status == StatusPedido.Pendente)
    .ToListAsync();
```

**3. Em APIs, representando opções fixas** (tipo enum de perfil de usuário, tipo de pagamento, prioridade de chamado):

```csharp
public enum PerfilUsuario
{
    Admin,
    Editor,
    Visitante
}
```

### `[Flags]` — enum como combinação de valores (menos comum, mas cai em entrevista)

```csharp
[Flags]
public enum Permissoes
{
    Nenhuma = 0,
    Ler = 1,
    Escrever = 2,
    Excluir = 4,
    Admin = Ler | Escrever | Excluir
}

Permissoes minhasPermissoes = Permissoes.Ler | Permissoes.Escrever;
```

Isso usa os valores em potências de 2 pra permitir combinar múltiplos valores num único enum, usando operadores bit a bit. É um recurso mais avançado — não é o dia a dia comum, mas aparece em sistemas de permissão.

### Resumindo pro mercado

`enum` é **muito usado** — praticamente todo sistema tem algum tipo de status, categoria ou tipo fixo (status de pedido, tipo de usuário, prioridade, etc.). É código limpo, seguro em tempo de compilação, e se integra bem com EF Core e com o `TryParse` que já vimos. Vale dominar bem.

![[Pasted image 20260903154240.png]]