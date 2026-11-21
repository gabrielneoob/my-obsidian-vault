A normalização é o processo de organizar os dados para reduzir redundâncias e dependências, dividindo tabelas em entidades menores. São diferentes formas normais (FN) que ajudam a estruturar os dados de forma eficiente.

- **Primeira Forma Normal (1FN)**:
    
- **Segunda Forma Normal (2FN)**:
    
- **Terceira Forma Normal (3FN)**:
    

## 1FN

Elimina grupos repetitivos e garante que cada coluna contenha valores atômicos.

```sqlite
-- não normalizado
CREATE TABLE "produtos" (
  "id" INTEGER PRIMARY KEY,
  "nome" TEXT
) STRICT;

CREATE TABLE "pedidos" (
  "id" INTEGER PRIMARY KEY,
  "produtos" TEXT,
  "criado" TEXT DEFAULT CURRENT_TIMESTAMP
) STRICT;

INSERT INTO "pedidos" ("produtos") VALUES ('[1,2,3]');
```

```sqlite
-- normalizado (1FN)
CREATE TABLE "produtos" (
  "id" INTEGER PRIMARY KEY,
  "nome" TEXT
) STRICT;

CREATE TABLE "pedidos" (
  "id" INTEGER PRIMARY KEY,
  "criado" TEXT DEFAULT CURRENT_TIMESTAMP
) STRICT;

CREATE TABLE "pedido_produtos" (
  "pedido_id" INTEGER,
  "produto_id" INTEGER,
  FOREIGN KEY ("pedido_id") REFERENCES "pedidos" ("id"),
  FOREIGN KEY ("produto_id") REFERENCES "produtos" ("id")
) STRICT;

INSERT INTO "pedidos" ("id") VALUES (1);

INSERT INTO "pedido_produtos" ("pedido_id", "produto_id") VALUES (1, 1), (1, 2), (1, 3);
```

## 2FN

Elimina dependências parciais em chaves compostas.

```sqlite
CREATE TABLE "usuarios" (
  "id" INTEGER PRIMARY KEY,
  "nome" TEXT
) STRICT;

CREATE TABLE "cursos" (
  "id" INTEGER PRIMARY KEY,
  "nome" TEXT
) STRICT;
```

```sqlite
-- não normalizado (2FN)
CREATE TABLE "certificados" (
  "usuario_id" INTEGER,
  "curso_id" INTEGER,
  "curso_nome" TEXT,
  FOREIGN KEY ("usuario_id") REFERENCES "usuarios" ("id"),
  FOREIGN KEY ("curso_id") REFERENCES "cursos" ("id"),
  PRIMARY KEY ("usuario_id", "curso_id")
) STRICT;
```

```sqlite
-- normalizado (2FN)
CREATE TABLE "certificados" (
  "usuario_id" INTEGER,
  "curso_id" INTEGER,
  FOREIGN KEY ("usuario_id") REFERENCES "usuarios" ("id"),
  FOREIGN KEY ("curso_id") REFERENCES "cursos" ("id"),
  PRIMARY KEY ("usuario_id", "curso_id")
) STRICT;
```

## 3FN

Elimina dependências transitivas, garantindo que não haja atributos que dependam de outros atributos não-chave.

```sqlite
-- não normalizado (3FN)
CREATE TABLE "usuarios" (
  "id" INTEGER PRIMARY KEY,
  "nome" TEXT,
  "tipo" TEXT CHECK ("tipo" IN ('usuario', 'admin')),
  "tipo_leitura" INTEGER CHECK ("tipo_leitura" IN (0, 1)),
  "tipo_escrita" INTEGER CHECK ("tipo_escrita" IN (0, 1))
) STRICT;
```

```sqlite
-- normalizado (3FN)
CREATE TABLE "usuarios" (
  "id" INTEGER PRIMARY KEY,
  "nome" TEXT,
  "tipo_id" INTEGER,
  FOREIGN KEY ("tipo_id") REFERENCES "tipos" ("id")
) STRICT;

CREATE TABLE "tipos" (
  "id" INTEGER PRIMARY KEY,
  "tipo" TEXT UNIQUE,
  "leitura" INTEGER CHECK ("leitura" IN (0, 1)),
  "escrita" INTEGER CHECK ("escrita" IN (0, 1))
) STRICT;
```

## Tabelas de Referência

Quando temos uma coluna que possui valores geralmente fixos e repetidos, como estados, tipos de usuário, estatus de pedido etc. Podemos criar uma tabela de referência para normalizar esses dados.

```sqlite
CREATE TABLE "status_pedido" (
  "id" INTEGER PRIMARY KEY,
  "nome" TEXT UNIQUE NOT NULL,
  "cor" TEXT NOT NULL,
  "encerrado" INTEGER NOT NULL CHECK ("encerrado" IN (0,1))
) STRICT;

INSERT INTO
  "status_pedido" ("nome", "cor", "encerrado")
VALUES
  ('aguardando', '#FFC107', 0),
  ('pago', '#17A2B8', 0),
  ('separando', '#007BFF', 0),
  ('enviado', '#6610F2', 0),
  ('entregue', '#28A745', 1),
  ('cancelado', '#DC3545', 1);

CREATE TABLE "pedidos" (
  "id" INTEGER PRIMARY KEY,
  "valor_total" INTEGER NOT NULL,
  "status_id" INTEGER NOT NULL,
  FOREIGN KEY ("status_id") REFERENCES "status_pedido" ("id")
) STRICT;

INSERT INTO
  "pedidos" ("valor_total", "status_id")
VALUES
  (100, 1), (200, 2), (150, 3);
```