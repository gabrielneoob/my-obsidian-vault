## Matemática

As funções matemáticas mais comuns no SQLite são:

- `COUNT()`
    
    Conta o número de linhas.
    
- `SUM()`
    
    Soma os valores de uma coluna numérica.
    
- `AVG()`
    
    Calcula a média dos valores de uma coluna numérica.
    
- `MIN()`
    
    Retorna o menor valor de uma coluna.
    
- `MAX()`
    
    Retorna o maior valor de uma coluna.
    

```sqlite
SELECT COUNT(*) FROM "produtos";
SELECT COUNT() FROM "produtos";
SELECT COUNT("categoria") FROM "produtos";

-- AS para renomear colunas
SELECT SUM("estoque") AS "total_estoque" FROM "produtos";
SELECT SUM("preco" * "estoque") AS "valor_total_estoque" FROM "produtos";

SELECT AVG("preco") FROM "produtos";

SELECT MIN("preco"), * FROM "produtos";
SELECT MAX("preco"), * FROM "produtos";
```

## Texto

As funções de texto mais comuns no SQLite são:

- `LENGTH()`
    
    Retorna o comprimento de uma string.
    
- `UPPER()`
    
    Converte uma string para maiúsculas.
    
- `LOWER()`
    
    Converte uma string para minúsculas.
    
- `SUBSTR()`
    
    Retorna uma parte de uma string.
    
- `TRIM()`
    
    Remove espaços em branco do início e do fim de uma string.
    

```sqlite
SELECT LENGTH("nome"), "nome" FROM "produtos";
SELECT UPPER("nome") FROM "produtos";
SELECT LOWER("nome") FROM "produtos";
SELECT SUBSTR("nome", 1, 5) FROM "produtos"; -- Pega os 5 primeiros caracteres
SELECT TRIM("nome") FROM "produtos";
```

## Data e Hora

As funções de data e hora mais comuns no SQLite são:

- `DATE()`
    
    Retorna a data atual ou converte uma string em data.
    
- `TIME()`
    
    Retorna a hora atual ou converte uma string em hora.
    
- `DATETIME()`
    
    Retorna a data e hora atual ou converte uma string em data e hora.
    
- `STRFTIME()`
    
    Formata uma data e hora em uma string.
    

```sqlite
SELECT DATE('now');

SELECT TIME('now'); -- UTC (+00:00)
SELECT TIME('now', '-03:00');
SELECT TIME('now', 'localtime');

SELECT DATETIME('now', '-03:00');

SELECT CURRENT_TIMESTAMP;

SELECT STRFTIME('%Y-%m-%d %H:%M', 'now');

-- Cálculo de datas
SELECT DATE('now', '+1 day'); -- Adiciona 1 dia
SELECT DATE('now', '-1 month'); -- Subtrai 1 mês
SELECT DATETIME('now', '+1 day', '-6 hours'); -- +1 dia e depois -3 h
SELECT DATE('2049-06-16', '+7 days'); -- 2025-06-23
SELECT TIME('12:00', '+90 minutes'); -- 13:30:00

SELECT * FROM "produtos"
WHERE "criado"
BETWEEN DATE('2049-01-01') AND DATE('2049-01-01', '+6 month');
```

## Uso das Funções

As funções podem ser usadas em `CREATE`, `SELECT`, `WHERE`, `INSERT` e mais.

```sqlite
CREATE TABLE "livros" (
  "id" INTEGER PRIMARY KEY,
  "nome" TEXT NOT NULL,
  "criado" TEXT NOT NULL DEFAULT (STRFTIME('%Y-%m-%d', 'now'))
) STRICT;

INSERT INTO
  "livros" ("nome")
VALUES
  (TRIM('   Aprendendo SQL  ')),
  (TRIM('Avançando em SQL '));

SELECT "nome", LENGTH("nome") AS "tamanho_nome"
FROM "livros"
WHERE "tamanho_nome" > 15;
```