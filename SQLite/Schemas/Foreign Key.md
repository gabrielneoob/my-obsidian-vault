Estabelece uma relação entre tabelas, garantindo a integridade referencial.

```sqlite
CREATE TABLE "cursos" (
  "id" INTEGER PRIMARY KEY,
  "nome" TEXT
) STRICT;

CREATE TABLE "aulas" (
  "id" INTEGER PRIMARY KEY,
  "curso_id" INTEGER,
  "nome" TEXT,
  FOREIGN KEY("curso_id") REFERENCES "cursos" ("id")
) STRICT;

INSERT INTO
  "aulas" ("curso_id", "nome")
VALUES
  (1, 'Fundamentos do HTML');

```

## CASCADE

Use o `CASCADE` para remover/atualizar automaticamente as linhas dependentes ao remover/atualizar uma linha referenciada.

```sqlite
CREATE TABLE "aulas" (
  "id" INTEGER PRIMARY KEY,
  "curso_id" INTEGER,
  "nome" TEXT,
  FOREIGN KEY("curso_id") REFERENCES "cursos" ("id") ON DELETE CASCADE ON UPDATE CASCADE
) STRICT;

UPDATE "cursos" SET "id" = 2 WHERE "id" = 1;
DELETE FROM "cursos" WHERE "id" = 2;
```