- São definições de métodos encapsulados, porém expondo uma sintaxe similar à de atributos e não de métodos

- Uma propriedade é um membro que oferece um mecanismo flexível para ler, gravar ou calcular o valor de um campo particular. As propriedades podem ser usadas como se fossem atributos públicos, mas na verdade elas são métodos especiais chamados "acessadores". Isso permite que os dados sejam acessados facilmente e ainda ajuda a promover a segurança e a flexibilidade dos métodos.

## Auto Properties

- É uma forma simplificada de se declarar propriedades que não necessitam lógicas particulares para as operações get e set.

```csharp
public double Preco { get; private set; }
```

### O objetivo real: controle, não bloqueio total

Se o objetivo fosse só "impedir alteração de fora", a solução mais simples seria deixar tudo `private` sem propriedade nenhuma — aí ninguém de fora acessaria nada, nem pra ler nem pra escrever. Mas isso quase nunca é o que você quer; geralmente você **quer permitir acesso**, só que de forma controlada, validada, ou restrita a um sentido só (leitura sim, escrita não, por exemplo).

Get/set existem principalmente pra resolver isso:

```csharp
public string Nome
{
    get => _nome;                          // permite ler de fora
    set                                     // permite escrever de fora
    {
        if (string.IsNullOrWhiteSpace(value))
            throw new ArgumentException("Nome não pode ser vazio");
        _nome = value;                      // mas só se passar na validação
    }
}
```

Aqui, de fora, **você pode sim** alterar `Nome`:

csharp

```csharp
produto.Nome = "Camiseta"; // funciona
produto.Nome = "";         // dispara exceção — bloqueado pela validação, não pela propriedade em si
```

Ou seja: a propriedade não bloqueia a alteração — ela **intercepta** a alteração e decide se aceita ou não.

### Os diferentes "níveis" de controle que dá pra ter

**1. Acesso livre total (equivale a campo público, mas ainda assim melhor)**

csharp

```csharp
public string Nome { get; set; }
```

Aqui você realmente não está restringindo nada — mas ainda ganha flexibilidade (se um dia precisar adicionar validação, muda só aqui dentro, sem quebrar quem já usa `produto.Nome = "X"` de fora).

**2. Leitura livre, escrita só de dentro da classe**

csharp

```csharp
public int Quantidade { get; private set; }
```

De fora: só lê. De dentro da classe (métodos como `AdicionarProdutos`): pode escrever.

**3. Leitura e escrita, mas com validação/regra de negócio**

csharp

```csharp
public string Nome
{
    get => _nome;
    set { /* validação */ _nome = value; }
}
```

De fora: pode ler e escrever, mas passa por regra.

**4. Só leitura, nunca escreve depois de criado**

csharp

```csharp
public string Nome { get; init; } // ou só { get; } setado via construtor
```

### Por que isso é melhor que campo público simples

A resposta curta pra "por que não deixar `public string nome;` direto?" é: porque um campo público **não tem como interceptar nada**. Não dá pra validar, não dá pra restringir só leitura, não dá pra logar quando muda, não dá pra fazer nada — é uma porta escancarada, sem trava, sem campainha.

csharp

```csharp
public string nome; // campo público — qualquer um faz p.nome = null; sem aviso
```

vs.

csharp

```csharp
public string Nome { get; private set; } // propriedade — você decide as regras
```

Mesmo quando a propriedade **não tem lógica nenhuma** (`get; set;` simples), ela já vale a pena, porque deixa a porta aberta pra adicionar controle depois **sem quebrar quem já usa a classe**. Se um dia você trocar um campo público por uma propriedade, todo código externo que fazia `produto.nome = "x"` teria que ser recompilado, mas se já era propriedade desde o início, a sintaxe de uso não muda nada.

### Resumindo a ideia certa

Não é "criamos get/set pra impedir alteração de fora" — é **"criamos get/set pra ter um ponto único de controle sobre como a leitura e a escrita acontecem"**. Às vezes esse controle resulta em bloqueio total de um lado (só `get`, sem `set` nenhum, ou `private set`), às vezes resulta em validação, às vezes não restringe nada mas deixa a porta pronta pra restringir no futuro.