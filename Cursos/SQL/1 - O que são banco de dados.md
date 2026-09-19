Um **banco de dados** é um sistema para gerenciar dados que nos permite:

- **Armazenar** dados de forma confiável
- **Recuperar** informações de maneira eficiente
- **Manipular** dados sistematicamente
  
Bancos de dados estão em todo lugar — e provavelmente você já trabalhou com aplicações que dependem deles!

Cada vez que um usuário faz login, busca um produto ou carrega seu perfil, uma consulta está sendo feita ao banco de dados por trás dos panos.
![[Pasted image 20260918144126.png]]
Além de alimentar aplicações, bancos de dados também são a base de **análise de dados e relatórios**.

Pense nos dashboards que executivos usam para tomar decisões — quantos usuários acessaram o app hoje, quais produtos vendem mais, qual é a receita do mês. **Todos esses números vêm de dados armazenados em bancos de dados.**

![[Pasted image 20260918144217.png]]

O tipo mais popular de banco de dados é o **banco de dados relacional**. Nele, os dados são organizados em **tabelas** — e cada tabela representa um tipo específico de entidade ou evento.
![[Pasted image 20260918144332.png]]


Aqui está a nossa tabela principal de produtos — ela contém informações sobre todos os itens disponíveis para venda no nosso e-commerce.

Tables são compostas de **linhas e colunas**. Vamos começar pelas linhas.

Cada **linha representa uma única entidade** — neste caso, um produto específico. Olhe, por exemplo, a primeira linha destacada aqui: ela contém todas as informações sobre os "Wireless Bluetooth Headphones" — o preço, a marca, a avaliação e tudo mais.

Em outros contextos você pode ouvir uma linha ser chamada de **"registro"** ou **"observação"** — são apenas nomes diferentes para a mesma coisa.

![[Pasted image 20260918144617.png]]

## Agora vamos às **colunas**.

Cada coluna **representa um atributo específico** da entidade — ou seja, uma propriedade ou característica dela. Repare na coluna `product_name` destacada aqui: ela armazena o nome de cada produto em todas as linhas.

Cada coluna também tem um **nome descritivo** que indica exatamente o que ela contém — `price`, `brand`, `rating`, e assim por diante.

Você pode ouvir uma coluna ser chamada de **"campo"** ou **"atributo"** — são termos equivalentes.
![[Pasted image 20260918144839.png]]

**Bancos de dados**

- Um **banco de dados** é um sistema para gerenciar dados que nos permite armazenar dados de forma confiável, recuperar informações de maneira eficiente e manipular dados sistematicamente.
    
- Bancos de dados impulsionam aplicações web, mobile e outras, bem como análise de dados e relatórios.
  
**Organização de Dados**

- Os dados em um banco de dados são organizados em **tabelas** com linhas e colunas.
- **Linhas** representam entidades ou eventos individuais.
- **Colunas** representam atributos ou propriedades específicas.

**Fundamentos de SQL**

- A Structured Query Language (**SQL**) é a linguagem de programação mais amplamente utilizada para trabalhar com dados em bancos de dados.
    
- Em seu uso mais comum, você escreve código SQL para solicitar dados de bancos de dados, e eles retornam os resultados de que você precisa.
    
- O SQL é muito mais simples do que as linguagens de programação de propósito geral porque foi projetado para um propósito específico: trabalhar com dados.
  
  
  ![[Pasted image 20260918172349.png]]
  
  Existem dois sistemas envolvidos, como você pode ver aqui:

- **Servidor de banco de dados**: O computador que **armazena e executa** o banco de dados
- **Cliente de banco de dados**: O software que roda **no seu computador** e permite que você se conecte ao servidor, escreva queries SQL, envie-as para execução e veja os resultados.

Vários clientes podem se conectar ao **mesmo servidor simultaneamente** e rodar queries ao mesmo tempo. Todos veem os mesmos dados.

Essa estrutura é chamada de **arquitetura cliente-servidor**.

**Arquitetura Cliente-Servidor**

- **Servidores de banco de dados** armazenam e gerenciam bancos de dados, enquanto os **clientes de banco de dados** se conectam aos servidores e enviam consultas.
- Vários usuários podem se conectar simultaneamente ao mesmo servidor de banco de dados por meio de vários tipos de clientes, incluindo aplicações web e softwares de desktop.