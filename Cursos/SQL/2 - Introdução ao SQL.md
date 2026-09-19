**SQL** (pronunciado "S-Q-L" ou "sequel") significa **Structured Query Language**, e é a linguagem de programação mais usada no mundo para trabalhar com dados em bancos de dados.

O uso mais comum é simples: você escreve um código SQL chamado de **consulta SQL** pedindo informações específicas ao banco de dados — e ele responde com os resultados que você solicitou. Exatamente como você vê aqui.
![[Pasted image 20260918143615.png]]

Para escrever e executar queries SQL, você precisa de um **cliente SQL**. Eles vêm em dois formatos:

- **Aplicações web**: ferramentas no navegador, sem nada para instalar. Para PostgreSQL, opções populares incluem o **pgAdmin** (interface web) e plataformas como o próprio DataCamp.
- **Aplicações desktop**: softwares instalados no seu computador com uma interface amigável. Para PostgreSQL, os mais usados são **DBeaver**, **TablePlus** e **DataGrip**.

O SQL que você escreve é **exatamente o mesmo** independentemente do cliente que usar!

Para se conectar a um banco de dados **PostgreSQL**, você precisa fornecer as seguintes informações ao seu cliente SQL:

- **Endereço do servidor**: onde o banco de dados está hospedado (URL ou endereço IP)
- **Nome de usuário**: sua conta de acesso
- **Senha**: sua senha de acesso
- **Nome do banco de dados**: qual banco de dados específico usar
- **Porta**: o PostgreSQL usa a porta **5432** por padrão

Se você for trabalhar em uma organização, precisará solicitar essas informações ao seu **administrador de banco de dados** (DBA). Se estiver usando um serviço de nuvem como **AWS RDS**, **Google Cloud SQL** ou **Azure**, essas credenciais são geradas na própria plataforma no momento em que você cria a instância do PostgreSQL.
