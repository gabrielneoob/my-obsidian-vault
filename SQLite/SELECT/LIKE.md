## LIKE

O operador `LIKE` é usado para comparar padrões em strings. Por padrão ele não é sensível a maiúsculas e minúsculas.

```sqlite
SELECT * FROM "produtos" WHERE "nome" LIKE 'impressora 3d mini';
```

## Wildcard (%)

`%`: Representa zero ou mais caracteres.

```sqlite
-- Encontra produtos que começam com "notebook"
SELECT * FROM "produtos" WHERE "nome" LIKE 'notebook%';
-- Encontra produtos que terminam com "pro"
SELECT * FROM "produtos" WHERE "nome" LIKE '%pro';
-- Encontra produtos que têm "3d" no meio do nome
SELECT * FROM "produtos" WHERE "nome" LIKE '%3d%';
```

## Wildcard (_)

`_`: Representa exatamente um caractere.

```sqlite
-- Encontra produtos com 1 caractere antes de "TB"
SELECT * FROM "produtos" WHERE "nome" LIKE '% _TB%';
```

## NOT LIKE

O operador `NOT LIKE` é usado para excluir padrões específicos.

```sqlite
SELECT * FROM "produtos" WHERE "nome" NOT LIKE '%pro%';
```