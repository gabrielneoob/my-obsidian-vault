- Se comunicar recebendo chamadas, devolvendo respostas HTTP.
- Pode se comunicar com uma variadade de softwares (site, app android, app windows e muito mais...)

### Interoperabilidade 
- Significa que nossa API não está nem aí pro tipo de software e tipo de chamada que está comunicando com ela, e mais ainda, ela não se importa com o tipo de linguagem de programação está se comunicando com ela, desde que se respeite um contrato que ela definiu.

### Três tipos de Contratos 
- Definir o protocolo de comunicação com a nossa API
	- Protocolo HTTP(GET, POST, DELETE,  PUT, PATCH)
	- Dados (vai receber e fornecer dados), qual tipo de formato ela vai devolver?(json, xml....)
	- Chamadas -> cada funcionalidade vai estar sendo atribuída para uma **url**

### Métodos HTTP
- **POST** - Criar um registro
- **GET** - Pegar um registro
- **DELETE** - Deletando um registro
- **PUT** - Alterar todas as propriedades de um registro
- **PATCH** - Atualizar algumas propriedades de um registro


Uma url pode reaproveitar varios metodos, porém não pode repetir o mesmo método

![[Pasted image 20260921163939.png]]

API é uma interface que expõe funcionalidades ou dados de um sistema, permitindo que outros sistemas (ou o frontend) interajam com ele sem precisar conhecer os detalhes internos de implementação.