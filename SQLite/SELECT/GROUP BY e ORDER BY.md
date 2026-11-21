## ORDER BY

Ordena os resultados de uma consulta.

```sqlite
-- ASC (ascendente) é o padrão
SELECT * FROM "produtos" ORDER BY "preco" ASC;
SELECT * FROM "produtos" ORDER BY "preco" DESC;

-- primeiro a categoria, depois preço
SELECT * FROM "produtos" ORDER BY "categoria" ASC, "preco" ASC;

-- ordena por data
SELECT * FROM "produtos" ORDER BY "criado" DESC;
```

## GROUP BY

Agrupa os resultados de uma consulta.

```sqlite
SELECT "categoria", COUNT(*) AS "total" FROM "produtos" GROUP BY "categoria";
SELECT "categoria", AVG("preco") AS "preco_medio" FROM "produtos" GROUP BY "categoria";

-- GROUP BY e ORDER BY juntos
SELECT "categoria", COUNT(*) AS "total"
FROM "produtos" GROUP BY "categoria" ORDER BY "total" DESC;

--- Data por ANO
SELECT STRFTIME('%Y', "criado") AS "ano", COUNT(*) AS "total"
FROM "produtos" GROUP BY "ano";
```

## HAVING

Filtra os resultados de uma consulta após o agrupamento. O `HAVING` funciona como o `WHERE` após o `GROUP BY`.

```sqlite
SELECT "categoria", COUNT(*) AS "total"
FROM "produtos" GROUP BY "categoria"
HAVING "total" > 1;

SELECT "categoria", AVG("preco") AS "preco_medio"
FROM "produtos" GROUP BY "categoria"
HAVING "preco_medio" > 70000;
```