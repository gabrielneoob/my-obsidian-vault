
## Microsserviços

### O que você acha de microsserviços?
R: É bem usado, principalmente onde tem muitos times grandes ou partes do sistema com escala bem diferente entre si. Mas hoje tem uma visão mais madura no mercado, depois de vários casos de empresas que adotaram cedo demais e sofreram com a complexidade sem precisar. A decisão certa depende do problema real do time, não é sempre a melhor escolha por padrão

### Benenficios de se utilizar uma arquitetura de microsserviços?
R: Os ganhos principais são escalar cada parte de forma independente, fazer deploy sem depender dos outros times, e isolar falha, então um serviço caindo não derruba o sistema inteiro. Mas esses ganhos só compensam o custo de complexidade quando o time e o sistema já são grandes o bastante para sentir esses problemas de verdade.

- Três motivos para usar microsserviços
1- **Escalabilidade Independente**: Você escala um serviço sem depender ou afetar os outros

2- **Deploy independente**: Você pode lançar um deploy sem depender de outro serviço

3 - **Isolamento de falha**: Se um serviço falhar, não afeta os outros serviços

"Arquitetura em camadas: o controller recebia a requisição e chamava o service, o service tinha a regra de negócio, e o repository acessava o banco com Prisma. Cada camada só falava com a de baixo, o que deixava fácil saber onde mexer quando precisava mudar algo."

## Me explica a arquitetura, do front ao banco." → arquitetura em camadas, microsserviços, contrato de API
R: De forma geral, o front era em Nextjs, consumindo um back-end divido por microsserviços com Nestjs, cada microsserviço tinha o seu próprio domínio, como Catalogo, pedidos, usuário, pagamentos e Programa de fidelidade

No front era uma arquitetura monolitica modularizada, onde cada domínio tinha o seu módulo, Catalogo tinha seu componentes e chamdas de API próprias

A comunicação entre front e back era via API Rest, com contrato JSON.

E também dentro de cada microsserviço, a estrutura era em camadas: o controller recebia a requisição, o service tinha a regra de negocio, e o repository acessava o banco com Prisma. Cada serviço tinha seu próprio banco

No meu dia a dia eu atuava na Squad de Catálogo, criando e mantendo os endpoints REST que a gente consumia no front, como listagem e detalhe de produto

###