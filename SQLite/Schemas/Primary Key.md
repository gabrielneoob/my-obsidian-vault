Defina uma coluna como chave primária, que deve ser única e não nula

```sqlite
CREATE TABLE "cursos" (
	"id" INTEGER PRIMARY KEY,
	"nome" TEXT,
	"preco" INTEGER
) STRICT;

INSERT INTO
	"cursos" ("nome", "preco")
VALUES
	('HTML', 1000);
```

### RowId

Toda tabela tem uma coluna oculta chamada rowid, que é um identificador único para cada linha.

Se você não definir uma chave primária, o SQLite cria automaticamente uma coluna **rowid**

Se você definir uma coluna como **INTEGER PRIMARY KEY**, esla se torna um alias para a coluna rowid, issno não acontece caso use **INT**.