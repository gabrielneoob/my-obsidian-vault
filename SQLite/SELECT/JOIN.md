Agrega dados de duas ou mais tabelas com base em uma condição. O padrão do JOIN é o INNER JOIN, que retorna apenas as linhas que têm correspondência em ambas as tabelas. Pode usar `JOIN, INNER JOIN ou apenas a vírgula ,`.

```sqlite
SELECT * FROM "lessons_completed"
JOIN "users" ON "lessons_completed"."user_id" = "users"."id";

SELECT "users"."name", "lessons_completed"."lesson_id" FROM "lessons_completed"
JOIN "users" ON "lessons_completed"."user_id" = "users"."id";

SELECT "u"."name", "lc"."lesson_id" FROM "lessons_completed" AS "lc"
JOIN "users" AS "u" ON "lc"."user_id" = "u"."id";
```

## Múltiplos JOINs

Podemos fazer múltiplos JOINs para agregar dados de várias tabelas. Se o nome da coluna for o mesmo em ambas as tabelas, é necessário usar um alias `AS`.

```sqlite
SELECT "u"."name", "l"."title" AS "lesson_title", "c"."title" AS "course_title"
FROM "lessons_completed" AS "lc"
JOIN "users" AS "u" ON "lc"."user_id" = "u"."id"
JOIN "lessons" AS "l" ON "lc"."lesson_id" = "l"."id"
JOIN "courses" AS "c" ON "lc"."course_id" = "c"."id"
WHERE "u"."email" = 'carlos@email.com' AND "c"."slug" = 'html-para-iniciantes';
```

## LEFT JOIN

O `LEFT JOIN` retorna todas as linhas da tabela à esquerda `lessons` e as correspondências da tabela à direita `lessons_completed`. Se não houver correspondência, os valores da tabela à direita serão NULL.

```sqlite
SELECT "lc"."user_id", "l"."title", "lc"."completed"
FROM "lessons" AS "l"
LEFT JOIN "lessons_completed" AS "lc"
ON "lc"."lesson_id" = "l"."id" AND "lc"."user_id" = 1;
```

## SELF JOIN

O `SELF JOIN` é um JOIN de uma tabela consigo mesma. É útil para comparar linhas dentro da mesma tabela e encontrar valores duplicados.

```sqlite
SELECT "a"."id", "a"."slug"
FROM "lessons" AS "a"
JOIN "lessons" AS "b" ON "a"."slug" = "b"."slug"
WHERE "a"."id" != "b"."id";
```