No dia a dia, eu fazia parte do squad de Catálogo, trabalhando dentro de um framework Scrum , com sprints quinzenais

Minha rotina começava pela daily, onde a gente alinhava o que cada um estava fazendo e se tinha algum impedimento. Pegava as tarefas que vinham do backlog dentro do jira, que eram refinadas antes de entrar na sprint.

No trabalho em si, eu criava e mantinha endpoints REST do serviço de Catálogo, e consumia esses endpoints no front na página de catalogos. 

No back-end seguindo a estrutura em camadas: controller recebendo a requisição, service com a regra de negócio, e repository acessando o banco com Prisma.

Já no front seguindo a estrutuda de modulos, cada categoria tinha seu módulo: catalogo, programa-fidelidade

Depois de desenvolver, abria um PR pra code review, e quando aprovado ia pra homologação, onde o QA testava antes de ir pra produção.

No fim da sprint, tinha a review, pra mostrar o que foi entregue, e a retro, pra melhorar o processo.


 e eu participava desse refinamento levantando dúvida técnica e ajudando a estimar

Exemplo: Uma vez a história pedia ajustar a listagem de produtos de uma categoria. No refinamento, notei que a query não tinha paginação, e uma categoria como Banheiro tem muito produto, então ia sobrecarregar. Levantei isso, e o time incluiu a paginação no escopo da própria tarefa, em vez de deixar pra depois