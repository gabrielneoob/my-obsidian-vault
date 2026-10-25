# Cheatsheet: Prisma ORM 7 (Node + TypeScript + PostgreSQL)

Referência rápida para o dia a dia. Os exemplos usam o projeto `users-system` (`User` e `Notification`).

> **Segurança:** URL do banco, senhas e segredos ficam **sempre** no `.env` (que está no `.gitignore`). Versione só o `.env.example`, com valores fictícios.

---

## 1. Visão geral

| Peça | Papel |
|---|---|
| `prisma/schema.prisma` | Define models, enums, relações e o generator (**sem** a URL do banco no Prisma 7) |
| `prisma.config.ts` | Configuração da CLI: caminho do schema, URL do banco, migrations, seed |
| Prisma Client | Código gerado a partir do schema, usado para consultar o banco |
| Driver adapter | **Obrigatório no Prisma 7**: liga o Client ao driver do banco (`@prisma/adapter-pg` + `pg`) |
| Migrations | Histórico versionado das mudanças de schema (`prisma/migrations/`) |

---

## 2. Instalação e setup (Prisma 7 + Postgres)

```bash
npm i @prisma/client @prisma/adapter-pg pg dotenv
npm i -D prisma typescript tsx @types/node @types/pg
npx prisma init
```

### `.env` (nunca versionado)

```env
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=uma_senha_forte
POSTGRES_DB=users_system
POSTGRES_PORT=5433

DATABASE_URL="postgresql://seu_usuario:uma_senha_forte@localhost:5433/users_system"
```

### `.env.example` (versionado, sem valores reais)

```env
DATABASE_URL="postgresql://USER:PASSWORD@localhost:5433/DB_NAME"
```

### `prisma/schema.prisma`

```prisma
generator client {
  provider = "prisma-client"
  output   = "../generated/prisma"
}

datasource db {
  provider = "postgresql"
}
```

- O `output` é **obrigatório** no generator `prisma-client`.
- A URL **não** fica mais no `datasource`; ela vai no `prisma.config.ts`.
- Adicione `generated/` ao `.gitignore`.

### `prisma.config.ts`

```ts
import "dotenv/config";
import { defineConfig, env } from "prisma/config";

export default defineConfig({
  schema: "prisma/schema.prisma",
  migrations: {
    path: "prisma/migrations",
    seed: "tsx prisma/seed.ts",
  },
  datasource: {
    url: env("DATABASE_URL"),
  },
});
```

> O Prisma 7 **não carrega o `.env` automaticamente**. Por isso o `import "dotenv/config"` no topo.

### Client com driver adapter (`src/shared/prisma.ts`)

```ts
import "dotenv/config";
import { PrismaPg } from "@prisma/adapter-pg";
import { PrismaClient } from "../../generated/prisma/client.js";

const connectionString = process.env.DATABASE_URL;
if (!connectionString) {
  throw new Error("DATABASE_URL não definida");
}

const adapter = new PrismaPg({ connectionString });

export const prisma = new PrismaClient({ adapter });
```

Dicas:

- Crie **um único** `PrismaClient` e reuse em todo o app (o seu roteiro pede isso em `shared/`).
- Com `"module": "nodenext"`, imports relativos precisam da extensão `.js` (mesmo em arquivos `.ts`).
- Com `verbatimModuleSyntax`, importe só tipos com `import type { ... }`.
- Alternativa ao `dotenv`: rodar com `tsx --env-file=.env src/server.ts`.

---

## 3. Comandos da CLI

| Comando | O que faz |
|---|---|
| `npx prisma init` | Cria `schema.prisma`, `prisma.config.ts` e `.env` |
| `npx prisma generate` | Gera o Prisma Client a partir do schema |
| `npx prisma validate` | Valida o schema |
| `npx prisma format` | Formata o schema |
| `npx prisma migrate dev --name <nome>` | Cria e aplica uma migration (desenvolvimento) |
| `npx prisma migrate deploy` | Aplica migrations pendentes (CI/produção) |
| `npx prisma migrate status` | Mostra o estado das migrations |
| `npx prisma migrate reset` | Apaga o banco, reaplica tudo e roda o seed (**só em dev**) |
| `npx prisma migrate resolve` | Marca uma migration como aplicada ou revertida |
| `npx prisma migrate diff` | Compara schemas/bancos e gera o SQL da diferença |
| `npx prisma db push` | Sincroniza schema com o banco **sem** migration (prototipagem) |
| `npx prisma db pull` | Banco existente → schema |
| `npx prisma db seed` | Executa o seed configurado |
| `npx prisma db execute` | Executa SQL de um arquivo |
| `npx prisma studio` | Interface visual para ver e editar dados |

Lembrete do Prisma 7: rode `prisma generate` e `prisma db seed` **explicitamente**; eles não são executados automaticamente após o `migrate dev`.

Fluxo comum:

```bash
# 1. editar schema.prisma
npx prisma format
npx prisma migrate dev --name add_notifications
npx prisma generate
```

---

## 4. Schema: models e campos

```prisma
model User {
  id           String   @id @default(uuid()) @db.Uuid
  name         String
  email        String   @unique
  passwordHash String   @map("password_hash")
  createdAt    DateTime @default(now()) @map("created_at")
  updatedAt    DateTime @updatedAt @map("updated_at")

  @@map("users")
}
```

### Tipos escalares

| Prisma | Postgres | Uso |
|---|---|---|
| `String` | `text` | Textos |
| `Int` | `integer` | Inteiros |
| `BigInt` | `bigint` | Inteiros grandes |
| `Float` | `double precision` | Decimais aproximados |
| `Decimal` | `numeric` | Dinheiro e valores exatos |
| `Boolean` | `boolean` | Verdadeiro/falso |
| `DateTime` | `timestamp(3)` | Datas |
| `Json` | `jsonb` | Objetos JSON |
| `Bytes` | `bytea` | Binário |

Tipos nativos: `@db.VarChar(255)`, `@db.Uuid`, `@db.Timestamptz(3)`, `@db.Decimal(10, 2)`, `@db.Text`.

### Modificadores

| Sintaxe | Significado |
|---|---|
| `String?` | Opcional (aceita `null`) |
| `String[]` | Lista (array no Postgres) |

### Atributos de campo

| Atributo | Significado |
|---|---|
| `@id` | Chave primária |
| `@default(uuid())` | UUID automático |
| `@default(autoincrement())` | Inteiro sequencial |
| `@default(now())` | Data atual na criação |
| `@default(cuid())` | ID cuid |
| `@updatedAt` | Atualiza sozinho a cada update |
| `@unique` | Valor único |
| `@map("coluna")` | Nome da **coluna** no banco |
| `@db.*` | Tipo nativo do banco |
| `@relation(...)` | Define uma relação |

### Atributos de bloco

| Atributo | Significado |
|---|---|
| `@@map("tabela")` | Nome da **tabela** no banco |
| `@@id([a, b])` | Chave primária composta |
| `@@unique([a, b])` | Unicidade composta |
| `@@index([a, b])` | Índice |
| `@@schema("nome")` | Schema Postgres do model (multi-schema) |

### `@map` e `@@map`

Mantêm o código em `camelCase` e o banco em `snake_case`. No Prisma Client você continua usando os nomes do schema (`user.passwordHash`); os nomes mapeados só aparecem no banco e em SQL puro.

---

## 5. Enums

```prisma
enum NotificationStatus {
  PENDING @map("pending")
  SENT    @map("sent")
  FAILED  @map("failed")

  @@map("notification_status")
}
```

---

## 6. Relações

### 1:N com relation

```prisma
model User {
  id            String         @id @default(uuid()) @db.Uuid
  notifications Notification[]

  @@map("users")
}

model Notification {
  id        String             @id @default(uuid()) @db.Uuid
  userId    String             @map("user_id") @db.Uuid
  type      String
  status    NotificationStatus @default(PENDING)
  error     String?
  createdAt DateTime           @default(now()) @map("created_at")
  sentAt    DateTime?          @map("sent_at")

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@index([userId])
  @@map("notifications")
}
```

### 1:N sem relation (só guarda o `userId`, menos acoplamento entre módulos)

```prisma
model Notification {
  id     String @id @default(uuid()) @db.Uuid
  userId String @map("user_id") @db.Uuid

  @@index([userId])
  @@map("notifications")
}
```

Trade-off: com relation você ganha `include` e integridade referencial no banco, mas acopla os módulos. Sem relation, os módulos ficam independentes, e a integridade passa a ser responsabilidade da aplicação.

### `onDelete` / `onUpdate`

| Valor | Comportamento |
|---|---|
| `Cascade` | Apaga/atualiza os filhos junto |
| `Restrict` | Bloqueia se houver filhos |
| `NoAction` | Igual ao Restrict (checado no fim) |
| `SetNull` | Define a FK como `null` (campo precisa ser opcional) |
| `SetDefault` | Define o valor padrão |

### 1:1

```prisma
model User {
  id      String   @id @default(uuid())
  profile Profile?
}

model Profile {
  id     String @id @default(uuid())
  userId String @unique
  user   User   @relation(fields: [userId], references: [id])
}
```

### N:N implícita (o Prisma cria a tabela de junção)

```prisma
model Post {
  id   String @id @default(uuid())
  tags Tag[]
}

model Tag {
  id    String @id @default(uuid())
  posts Post[]
}
```

### N:N explícita (quando a junção precisa de campos extras)

```prisma
model PostTag {
  postId String
  tagId  String
  post   Post   @relation(fields: [postId], references: [id])
  tag    Tag    @relation(fields: [tagId], references: [id])

  @@id([postId, tagId])
}
```

---

## 7. Prisma Client: consultas (CRUD)

```ts
import { prisma } from "../shared/prisma.js";
```

### Criar

```ts
const user = await prisma.user.create({
  data: { name: "Ana", email: "ana@email.com", passwordHash: hash },
});

await prisma.user.createMany({
  data: [
    { name: "A", email: "a@email.com", passwordHash: h1 },
    { name: "B", email: "b@email.com", passwordHash: h2 },
  ],
  skipDuplicates: true,
});

const created = await prisma.user.createManyAndReturn({ data: [/* ... */] });
```

### Ler

```ts
await prisma.user.findUnique({ where: { id } });           // por campo @id/@unique
await prisma.user.findUniqueOrThrow({ where: { id } });    // lança erro se não achar
await prisma.user.findFirst({ where: { name: "Ana" } });
await prisma.user.findFirstOrThrow({ where: { name: "Ana" } });
await prisma.user.findMany();
```

### Atualizar

```ts
await prisma.user.update({ where: { id }, data: { name: "Novo nome" } });
await prisma.user.updateMany({ where: { name: "Ana" }, data: { name: "Ana M." } });

// upsert: cria se não existir, atualiza se existir
await prisma.user.upsert({
  where: { email },
  update: { name },
  create: { name, email, passwordHash },
});

// incremento atômico
await prisma.post.update({ where: { id }, data: { views: { increment: 1 } } });
```

Operadores numéricos: `increment`, `decrement`, `multiply`, `divide`, `set`.

### Remover

```ts
await prisma.user.delete({ where: { id } });
await prisma.user.deleteMany({ where: { createdAt: { lt: new Date("2025-01-01") } } });
```

### Contar e agregar

```ts
await prisma.user.count();
await prisma.user.count({ where: { name: { startsWith: "A" } } });

await prisma.order.aggregate({
  _sum: { total: true },
  _avg: { total: true },
  _min: { total: true },
  _max: { total: true },
  _count: true,
});

await prisma.order.groupBy({
  by: ["status"],
  _count: { _all: true },
  _sum: { total: true },
  having: { total: { _sum: { gt: 1000 } } },
});
```

---

## 8. Filtros (`where`)

```ts
await prisma.user.findMany({
  where: {
    email: { contains: "@gmail.com", mode: "insensitive" },
    name: { startsWith: "A" },
    createdAt: { gte: new Date("2026-01-01"), lt: new Date("2027-01-01") },
    id: { in: [id1, id2] },
    NOT: { name: "Admin" },
    OR: [{ name: "Ana" }, { name: "Bia" }],
    AND: [{ email: { endsWith: ".com" } }],
  },
});
```

| Operador | Uso |
|---|---|
| `equals`, `not` | Igualdade / diferença |
| `in`, `notIn` | Lista de valores |
| `lt`, `lte`, `gt`, `gte` | Comparações |
| `contains`, `startsWith`, `endsWith` | Texto |
| `mode: "insensitive"` | Ignora maiúsculas/minúsculas (Postgres) |
| `AND`, `OR`, `NOT` | Combinações lógicas |
| `is`, `isNot` | Relação 1:1 / N:1 |
| `some`, `every`, `none` | Relação 1:N |

Filtro por relação:

```ts
// usuários que têm ao menos uma notificação com falha
await prisma.user.findMany({
  where: { notifications: { some: { status: "FAILED" } } },
});
```

Valores nulos: `{ error: null }` e `{ error: { not: null } }`.

---

## 9. `select`, `include` e `omit`

```ts
// select: escolhe exatamente os campos
await prisma.user.findMany({ select: { id: true, name: true, email: true } });

// include: traz os campos do model + relações
await prisma.user.findUnique({
  where: { id },
  include: { notifications: true },
});

// omit: tira campos (ex.: nunca devolver o hash)
await prisma.user.findMany({ omit: { passwordHash: true } });

// aninhado
await prisma.user.findMany({
  select: {
    id: true,
    notifications: { select: { status: true }, where: { status: "FAILED" }, take: 5 },
  },
});
```

Não combine `select` e `include` no mesmo nível. Para nunca retornar o hash da senha, use `omit` ou `select` explícito (uma exigência do seu roteiro na Fase 6).

---

## 10. Ordenação e paginação

```ts
await prisma.user.findMany({
  orderBy: [{ createdAt: "desc" }, { name: "asc" }],
  skip: 20,   // offset
  take: 10,   // limite
});

// paginação por cursor (melhor para listas grandes)
await prisma.user.findMany({
  take: 10,
  skip: 1,                    // pula o próprio cursor
  cursor: { id: lastId },
  orderBy: { id: "asc" },
});

// valores distintos
await prisma.user.findMany({ distinct: ["name"] });
```

---

## 11. Escritas aninhadas (nested writes)

```ts
// criar o pai e os filhos juntos
await prisma.user.create({
  data: {
    name: "Ana",
    email: "ana@email.com",
    passwordHash: hash,
    notifications: {
      create: [{ type: "welcome" }],
    },
  },
  include: { notifications: true },
});

// conectar a um registro existente
await prisma.notification.create({
  data: { type: "welcome", user: { connect: { id: userId } } },
});

// atualizar filhos
await prisma.user.update({
  where: { id },
  data: {
    notifications: {
      updateMany: { where: { status: "PENDING" }, data: { status: "FAILED" } },
      deleteMany: { status: "SENT" },
    },
  },
});
```

Operações aninhadas: `create`, `createMany`, `connect`, `connectOrCreate`, `disconnect`, `set`, `update`, `updateMany`, `upsert`, `delete`, `deleteMany`.

---

## 12. Transações

```ts
// 1) Sequencial: tudo ou nada
const [user, notification] = await prisma.$transaction([
  prisma.user.create({ data: { /* ... */ } }),
  prisma.notification.create({ data: { /* ... */ } }),
]);

// 2) Interativa: com lógica entre as operações
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({ data: { /* ... */ } });
  await tx.notification.create({ data: { userId: user.id, type: "welcome" } });
});
```

Dentro da transação interativa use **`tx`**, não `prisma`. Se lançar um erro, tudo é revertido. Evite chamadas de rede lentas dentro dela, pois ela segura a conexão.

Opções: `prisma.$transaction(fn, { maxWait: 5000, timeout: 10000 })`.

---

## 13. SQL puro

```ts
import { Prisma } from "../../generated/prisma/client.js";

// leitura (tagged template: seguro contra SQL injection)
const rows = await prisma.$queryRaw<{ id: string }[]>`
  SELECT id FROM users WHERE email = ${email}
`;

// escrita (retorna o número de linhas afetadas)
const affected = await prisma.$executeRaw`
  UPDATE users SET name = ${name} WHERE id = ${id}
`;

// composição segura
const where = Prisma.sql`WHERE email = ${email}`;
await prisma.$queryRaw`SELECT * FROM users ${where}`;
```

Nunca monte SQL concatenando strings com entrada do usuário. Evite `$queryRawUnsafe`/`$executeRawUnsafe` com dados externos. Em SQL puro, use os nomes **mapeados** (`password_hash`, `users`).

---

## 14. Tratamento de erros

```ts
import { Prisma } from "../../generated/prisma/client.js";

try {
  await prisma.user.create({ data });
} catch (err) {
  if (err instanceof Prisma.PrismaClientKnownRequestError) {
    if (err.code === "P2002") {
      // violação de unique (ex.: email duplicado) → 409
    }
    if (err.code === "P2025") {
      // registro não encontrado (update/delete) → 404
    }
  }
  throw err;
}
```

| Código | Significado | Status HTTP sugerido |
|---|---|---|
| `P2002` | Violação de unique constraint | 409 |
| `P2003` | Violação de foreign key | 409 ou 400 |
| `P2025` | Registro não encontrado | 404 |
| `P2000` | Valor longo demais para a coluna | 400 |
| `P1001` | Banco inacessível | 503 |

`err.meta?.target` indica quais campos causaram o `P2002`.

Outros erros: `PrismaClientValidationError` (query inválida), `PrismaClientInitializationError` (falha ao conectar).

---

## 15. Logs e ciclo de vida

```ts
const prisma = new PrismaClient({
  adapter,
  log: ["warn", "error"],            // em dev: ["query", "info", "warn", "error"]
});

// encerrar a conexão no shutdown
process.on("SIGINT", async () => {
  await prisma.$disconnect();
  process.exit(0);
});
```

---

## 16. Seed

`prisma/seed.ts`:

```ts
import "dotenv/config";
import { prisma } from "../src/shared/prisma.js";

async function main() {
  await prisma.user.upsert({
    where: { email: "admin@exemplo.com" },
    update: {},
    create: { name: "Admin", email: "admin@exemplo.com", passwordHash: "hash-de-exemplo" },
  });
}

main()
  .catch((e) => {
    console.error(e);
    process.exitCode = 1;
  })
  .finally(() => prisma.$disconnect());
```

Registre no `prisma.config.ts` (`migrations.seed`) e rode `npx prisma db seed`. Use `upsert` para o seed poder rodar mais de uma vez. Não coloque senhas reais no seed.

---

## 17. Fluxos de migration

| Situação | Comando |
|---|---|
| Mudei o schema em desenvolvimento | `npx prisma migrate dev --name descricao` |
| Deploy / CI / produção | `npx prisma migrate deploy` |
| Prototipagem rápida (sem histórico) | `npx prisma db push` |
| Banco de desenvolvimento bagunçado | `npx prisma migrate reset` |
| Banco já existente, quero o schema | `npx prisma db pull` |

Boas práticas:

- Faça commit da pasta `prisma/migrations/`.
- Nunca edite uma migration já aplicada em outros ambientes; crie outra.
- `migrate reset` apaga todos os dados. **Nunca** em produção.
- Dê nomes descritivos (`add_notifications`, `add_user_email_index`).
- Em produção/CI use só `migrate deploy`.

---

## 18. Estrutura sugerida (monólito modular)

```
src/
  shared/
    prisma.ts          <- PrismaClient único
  modules/
    users/
      users.repository.ts   <- único lugar que usa o Prisma
generated/
  prisma/              <- client gerado (não versionar)
prisma/
  schema.prisma
  migrations/
  seed.ts
prisma.config.ts
```

Regra do roteiro: todo acesso a dados fica atrás do **repository**. O service não conhece o Prisma, o que permite trocar o banco ou criar uma versão em memória para testes.

Exemplo de repository:

```ts
import { prisma } from "../../shared/prisma.js";

export const usersRepository = {
  findById: (id: string) =>
    prisma.user.findUnique({ where: { id }, omit: { passwordHash: true } }),

  findByEmail: (email: string) =>
    prisma.user.findUnique({ where: { email } }),

  create: (data: { name: string; email: string; passwordHash: string }) =>
    prisma.user.create({ data, omit: { passwordHash: true } }),
};
```

---

## 19. Problemas comuns

| Sintoma | Causa provável | Solução |
|---|---|---|
| `DATABASE_URL` não encontrada na CLI | `.env` não é carregado automaticamente | `import "dotenv/config"` no `prisma.config.ts` |
| `Cannot find module '../generated/...'` | Client não foi gerado | `npx prisma generate` |
| Erro de import sem `.js` | `module: nodenext` exige extensão | Use `./arquivo.js` nos imports relativos |
| Client sem adapter falha ao instanciar | Prisma 7 exige driver adapter | Use `new PrismaClient({ adapter })` |
| Erro de autenticação ao conectar | Senha/porta diferentes do volume já criado | Confira `.env`; volume antigo guarda credenciais antigas |
| `P2002` ao criar | Valor duplicado em campo `@unique` | Trate o erro e responda 409 |
| Tipos desatualizados após mudar o schema | Client antigo | `npx prisma generate` |
| Porta 5432 com erro de permissão (Windows) | Faixa reservada pelo Windows | Mapear outra porta no host (ex.: 5433) |

---

## 20. Resumo rápido

```bash
npx prisma init                              # começar
npx prisma format && npx prisma validate     # conferir o schema
npx prisma migrate dev --name <nome>         # criar + aplicar migration
npx prisma generate                          # gerar o client
npx prisma studio                            # ver os dados
npx prisma db seed                           # popular o banco
npx prisma migrate deploy                    # produção/CI
```

Documentação oficial: https://www.prisma.io/docs
