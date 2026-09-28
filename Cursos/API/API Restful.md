### API RESTful (uma espécie de API)

REST (Representational State Transfer) é um **estilo arquitetural** específico para construir APIs, criado por Roy Fielding em 2000. Uma API é "RESTful" quando segue certos princípios:

1. **Stateless** — cada requisição contém toda a informação necessária; o servidor não guarda estado de sessão entre chamadas
2. **Cliente-servidor** — separação clara de responsabilidades
3. **Interface uniforme** — usa recursos (resources) identificados por URIs, manipulados via verbos HTTP padrão:
    - `GET` → ler
    - `POST` → criar
    - `PUT/PATCH` → atualizar
    - `DELETE` → remover
4. **Representações** — os recursos trafegam em formatos como JSON ou XML
5. **Cacheable** — respostas podem indicar se são cacheáveis
6. **Sistema em camadas** — pode haver proxies, gateways, etc. sem o cliente saber

#### Exemplo prático

```
GET  /users/123      → busca o usuário 123
POST /users          → cria um novo usuário
PUT  /users/123      → atualiza o usuário 123
DELETE /users/123    → remove o usuário 123
```

Isso é diferente de, por exemplo, uma API estilo RPC, onde você teria algo como:

```
POST /getUser?id=123
POST /createUser
POST /updateUser
POST /deleteUser
```

Aqui tudo é `POST` e a "ação" fica no nome do endpoint, em vez de usar o verbo HTTP + o recurso — isso **não é RESTful**, mesmo rodando sobre HTTP.

#### Resumindo

||API|API RESTful|
|---|---|---|
|Escopo|Termo genérico, qualquer interface|Um tipo específico de API|
|Padrão|Não segue um padrão fixo|Segue os princípios REST|
|Protocolo|Pode usar qualquer protocolo|Tipicamente HTTP|
|Estrutura|Livre|Recursos + verbos HTTP + stateless|

Na prática, quando alguém fala "API" no contexto web hoje em dia, na maioria das vezes está se referindo a uma API REST (ou algo que tenta ser), mas nem toda API HTTP é de fato RESTful — muita gente usa o termo de forma solta pra descrever qualquer API JSON sobre HTTP, mesmo sem seguir todos os princípios do Fielding.