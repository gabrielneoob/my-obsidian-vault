## NOT NULL

O valor da coluna não pode ser nulo.

```sqlite
CREATE TABLE "usuario" (
  "id" INTEGER PRIMARY KEY,
  "nome" TEXT NOT NULL
) STRICT;
```

## UNIQUE

O valor da coluna deve ser único em relação às outras linhas da tabela.

```sqlite
CREATE TABLE "usuario" (
  "id" INTEGER PRIMARY KEY,
  "email" TEXT NOT NULL UNIQUE,
  "nome" TEXT NOT NULL
) STRICT;
```

Dá para aplicar em mais de uma coluna, criando uma chave única composta.

```sqlite
CREATE TABLE "certificados" (
  "id" INTEGER PRIMARY KEY,
  "pessoa_id" INTEGER NOT NULL,
  "curso_id" INTEGER NOT NULL,
  UNIQUE ("pessoa_id", "curso_id")
) STRICT;
```

## COLLATE

Define como a comparação de textos deve ser feita, por exemplo, se deve ser sensível a maiúsculas e minúsculas `NOCASE`.

Com o `COLLATE NOCASE` `Andre@email.com` é o mesmo que `andre@email.com`

```sqlite
CREATE TABLE "usuario" (
  "id" INTEGER PRIMARY KEY,
  "email" TEXT NOT NULL UNIQUE COLLATE NOCASE,
  "nome" TEXT NOT NULL
) STRICT;
```

## DEFAULT

Define um valor padrão para a coluna quando nenhum valor é fornecido.

```sqlite
CREATE TABLE "usuario" (
  "id" INTEGER PRIMARY KEY,
  "email" TEXT NOT NULL UNIQUE COLLATE NOCASE,
  "nome" TEXT NOT NULL,
  "tipo" TEXT NOT NULL DEFAULT 'usuario',
  "criado" TEXT DEFAULT CURRENT_TIMESTAMP
) STRICT;
```

## CHECK

Condição que deve ser verdadeira para que a linha seja inserida ou atualizada.

O `check` pode receber diferentes condições, como:

- `CHECK ("vitalicio" IN (0, 1))`
    
    Verifica se o valor é 0 ou 1.
    
- `CHECK ("preco" > 0)`
    
    Verifica se o preço é maior que 0.
    

```sqlite
CREATE TABLE "usuario" (
  "id" INTEGER PRIMARY KEY,
  "email" TEXT NOT NULL UNIQUE COLLATE NOCASE,
  "nome" TEXT NOT NULL,
  "tipo" TEXT NOT NULL DEFAULT 'usuario' CHECK ("tipo" IN ('usuario', 'admin')),
  "vitalicio" INTEGER NOT NULL DEFAULT 0 CHECK ("vitalicio" IN (0, 1)),
  "criado" TEXT DEFAULT CURRENT_TIMESTAMP
) STRICT;
```