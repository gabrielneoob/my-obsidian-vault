## BETWEEN

O operador `BETWEEN` é usado para verificar se um valor está dentro de um intervalo específico, incluindo os limites.

```sqlite
-- Para valores numéricos
SELECT * FROM "produtos" WHERE "preco" BETWEEN 10000 AND 20000;

-- Para datas
SELECT * FROM "produtos" WHERE "criado" BETWEEN '2049-06' AND '2049-08';
SELECT * FROM "produtos" WHERE "criado" NOT BETWEEN '2049-06' AND '2049-08';
```

## IN

O operador `IN` é usado para verificar se um valor está presente em uma lista de valores (array).

```sqlite
SELECT * FROM "produtos" WHERE "categoria" IN ('notebook', 'hardware');
SELECT * FROM "produtos" WHERE "categoria" NOT IN ('notebook', 'hardware');
SELECT * FROM "produtos" WHERE "id" IN (1, 5, 7);
SELECT * FROM "produtos" WHERE "id" NOT IN (1, 5, 7);
```