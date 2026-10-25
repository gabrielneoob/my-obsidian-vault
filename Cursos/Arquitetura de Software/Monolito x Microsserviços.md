
## Arquitetura baseada em monolitos
Um sistema que centraliza todas as funcionalidades dentro dele mesmo, isso significa que tudo roda dentro do mesmo processo. exemplo: Cadastro de clientes, processamento de pedidos, geraçao de relatorios... Está tudo no mesmo lugar.

Geralmente um monolito tem apenas um banco de dados para toda a aplicação e um repositório para o código fonte

Vantagens: Simples de desenvolver, tem menos custo de infraestrutura do que um microsserviço, mais facil de testar e escalar verticalmente e até horizontalmente

Desvantagens: 
- Se uma parte do sistema precisar de mais recursos que a outra, todas a partes do sistemas vão se precisar se escaladas também.
- Tem um acoplamento muito forte em sistema de código. 
- Dificuldade do em trabalho em equipe

## Arquitetura baseada em microsserviços
![[Pasted image 20261012144333.png]]
![[Pasted image 20261012144346.png]]

Vantagens:
- Cada microsserviço vai ter seu próprio banco de dados, seu próprio ciclo de vida e ainda pode ser desenvolvido em varias tecnologias diferentes.
- Ter times separados para cada microsserviço
- Cada microsserviço pode ser construído com a sua própria linguagem de programação

Desvantagens:
- Aumenta a complexidade Sistêmica exponencialmente 
- aplicar mecanismos de mensageria para se comunicar entre os serviços(Rabbitmq, SQS, Apache kafka)
- Dominar CQRS, EDA, Event Sourcing, DDD
