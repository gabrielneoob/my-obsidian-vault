R: De forma geral, o front era em Nextjs, consumindo um back-end divido por microsserviços com Nest, cada microsserviço tinha o seu próprio domínio, seu próprio banco de dados e suas regras.

No front era uma arquitetura monolítica modularizada, onde cada domínio tinha o seu módulo, Catalogo tinha seu componentes e chamdas de API próprias

A comunicação entre front e back era via API Rest, com contrato JSON.

E também dentro de cada microsserviço, a estrutura era em camadas: o controller recebia a requisição, o service tinha a regra de negocio, e o repository acessava o banco.

No meu dia a dia eu atuava na Squad de Catálogo, criando e mantendo os endpoints REST que a gente consumia no front, como listagem e detalhe de produto