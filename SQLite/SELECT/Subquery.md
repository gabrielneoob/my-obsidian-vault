Devem ser escritas entre parênteses e o seu resultado será usado para compor a query principal.

```sqlite
SELECT * FROM "produtos"
WHERE "preco" > (SELECT AVG("preco") FROM "produtos");

SELECT * FROM "lessons"
WHERE "course_id" = (
  SELECT "id" FROM "courses" WHERE "slug" = 'javascript-basico'
);
```

## WITH AS

Cria uma "subquery nomeada" (CTE - Common Table Expression), que pode ser referenciada na query principal. É uma tabela temporário.

```sqlite
WITH "preco_medio" AS (
  SELECT AVG("preco") AS "media" FROM "produtos"
)
SELECT * FROM "produtos"
WHERE "preco" > (SELECT "media" FROM "preco_medio");
```