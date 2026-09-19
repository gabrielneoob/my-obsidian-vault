```sql
SELECT *
FROM products;
```
R: Seleciona todos os dados da tabela de products

- **`SELECT`** é o comando SQL que diz ao banco de dados quais colunas você quer buscar.
- **`*`** significa "todas as colunas" — é um atalho para não precisar listar cada uma.
- **`FROM products`** diz de qual tabela os dados devem vir — no caso, `products`.
- **`;`** é o terminador da consulta. Ele sinaliza ao SQL que a instrução acabou.

Esse bloco de código completo é chamado de **SQL Query** (consulta SQL). E `SELECT` e `FROM` são os **SQL keywords** (palavras-chave SQL) — comandos reservados com funções específicas.

```SQL
SELECT id,
       name,
       rating
FROM products
ORDER BY rating;
```
R: Seleciona as colunas "id","name" e "rating" da tabela de "products", ordenando por "rating" de forma crescente ASC(padrão se não passar nenhum argumento no ORDER BY) 

```SQL
SELECT id,
       name,
       rating
FROM products
ORDER BY rating DESC;
```
R: Mesma query da de cima mas agora em ordem decrescente 

```SQL
SELECT id,
       name,
       rating
FROM products
ORDER BY rating DESC
LIMIT 10;
```
R: seleciona `id`, `name`, `rating` de `products`, ordena por `rating` decrescente, e o `LIMIT 10` **limita o resultado às 10 primeiras linhas** depois da ordenação (isso é importante: o `LIMIT` é aplicado _depois_ do `ORDER BY`, então você pega os 10 produtos com maior `rating`, não 10 linhas aleatórias).

- **LIMIT** - limita o resultado das linhas da query com o numero passado
	- Muitos bancos de dados na nuvem cobram pelo volume de dados processados — uma consulta sem `LIMIT` em uma tabela com milhões de registros pode ser lenta e cara. Além disso, se houver um erro na sua query, ela pode retornar muito mais dados do que o esperado. Usar `LIMIT` é uma forma de se proteger disso.


```SQL
SELECT DISTINCT category
FROM products;
```
R:`SELECT DISTINCT category` retorna os valores **únicos** (sem repetição) da coluna `category` na tabela `products` — se houver várias linhas com a mesma categoria, ela aparece só uma vez no resultado.


```SQL
SELECT DISTINCT category AS unique_categories  
FROM products;
```
R: seleciona os valores únicos da coluna `category` da tabela `products` (graças ao `DISTINCT`), e usa `AS unique_categories` para **renomear a coluna no resultado** (é um _alias_, só muda o nome de exibição, não altera a coluna original na tabela).
### Resumo:

### **Seleção de Colunas**

```sql
SELECT column_1,
       column_2
FROM table_1;
```


- Usamos `SELECT` para especificar quais colunas recuperar e `FROM` para especificar a tabela de onde recuperar.
- `SELECT column_1`: seleciona uma coluna
- `SELECT column_1, column_2`: seleciona múltiplas colunas
- `SELECT *`: seleciona todas as colunas
  
### **Ordenação**

```sql
SELECT column_1,
       column_2
FROM table_1
ORDER BY column_1 DESC;
```

Copy

- Usamos `ORDER BY` para ordenar as linhas por uma coluna específica.
- `ORDER BY column_1`: Ordem crescente (do menor para o maior A-Z, 0-9)
- `ORDER BY column_1 DESC`: Ordem decrescente (do maior para o menor Z-A, 9-0)

### **Limitação de Linhas**

```sql
SELECT *
FROM table_1
LIMIT 10;
```

Copy

- Usamos `LIMIT` para restringir o número de linhas retornadas por uma consulta.
- O `LIMIT` é colocado ao final da consulta e retorna as primeiras N linhas produzidas pela consulta.
- **Limitar é uma prática essencial porque evita consultas lentas e caras** e protege contra erros que podem retornar muito mais dados do que o esperado.

### **Encontrando Valores Únicos**

```sql
SELECT DISTINCT column_name
FROM table_name;
```

Copy

- Usamos o `DISTINCT` para recuperar apenas valores únicos de uma coluna, eliminando duplicatas.
- O `DISTINCT` é colocado imediatamente após o `SELECT`.

### **Aliases de Coluna**

```sql
SELECT column_1 AS alias_name,
       column_2
FROM table_1;
```

Copy

- A palavra-chave `AS` atribui nomes temporários às colunas nos resultados da consulta para melhorar a legibilidade.
- O alias aparece nos cabeçalhos das colunas, mas não altera o nome original da coluna no banco de dados.
- Aliases eficazes devem ser descritivos, consistentes e usar a convenção snake_case para seguir as melhores práticas.