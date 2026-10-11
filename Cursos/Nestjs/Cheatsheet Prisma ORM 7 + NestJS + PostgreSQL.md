# Cheatsheet Prisma ORM 7 + NestJS + PostgreSQL

Referência rápida pra uso diário. Comandos com pnpm.

## 1. Comandos do CLI

```bash
pnpm prisma init                         # cria prisma/ e config
pnpm prisma generate                     # gera o client (rodar após mudar o schema)
pnpm prisma migrate dev --name <nome>    # cria e aplica migration em dev
pnpm prisma migrate deploy               # aplica migrations pendentes em prod/CI
pnpm prisma migrate reset                # apaga o banco, reaplica tudo (só dev)
pnpm prisma migrate status               # mostra o estado das migrations
pnpm prisma db push                      # sincroniza schema sem criar migration (protótipo)
pnpm prisma db pull                      # gera o schema a partir de um banco existente
pnpm prisma db seed                      # roda o seed
pnpm prisma studio                       # interface visual dos dados
pnpm prisma format                       # formata o schema.prisma
pnpm prisma validate                     # valida o schema
pnpm prisma -v                           # versões (CLI e client devem ser iguais)
```

No Prisma 7, o `generate` não roda sozinho depois do `migrate dev`. Rode os dois.

## 2. Configuração

**`prisma.config.ts`** (raiz do projeto):

```ts
import 'dotenv/config'
import { defineConfig, env } from 'prisma/config'

export default defineConfig({
  schema: 'prisma/schema.prisma',
  datasource: { url: env('DATABASE_URL') },
})
```

**`.env`:**

```env
DATABASE_URL="postgresql://usuario:senha@localhost:5432/banco"
```

Caracteres especiais na senha (`@`, `#`, `/`) precisam ser codificados na URL.

## 3. Schema

```prisma
generator client {
  provider = "prisma-client"
  output   = "../generated/prisma"
}

datasource db {
  provider = "postgresql"
}

model Project {
  id          String   @id @default(uuid())
  name        String   @unique
  description String?
  status      Status   @default(ACTIVE)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  tasks       Task[]

  @@index([status])
  @@map("projects")
}

enum Status {
  ACTIVE
  ARCHIVED
}
```

### Tipos de campo

- `String`, `Int`, `BigInt`, `Float`, `Decimal`, `Boolean`, `DateTime`, `Json`, `Bytes`
- `?` torna opcional (`String?`) e `[]` cria lista (`String[]`, só no Postgres)

### Atributos de campo

- `@id`: chave primária
- `@default(...)`: valor padrão. Funções: `uuid()`, `cuid()`, `now()`, `autoincrement()`, `dbgenerated("...")`
- `@unique`: valor único
- `@updatedAt`: atualiza sozinho a cada update
- `@map("coluna")`: nome da coluna no banco
- `@db.VarChar(255)`, `@db.Text`: tipo nativo do Postgres

### Atributos de modelo

- `@@id([a, b])`: chave composta
- `@@unique([a, b])`: unicidade composta
- `@@index([a, b])`: índice
- `@@map("tabela")`: nome da tabela no banco

## 4. Relações

**Um pra muitos (1:N)**

```prisma
model Project {
  id    String @id @default(uuid())
  tasks Task[]
}

model Task {
  id        String  @id @default(uuid())
  title     String
  projectId String
  project   Project @relation(fields: [projectId], references: [id], onDelete: Cascade)

  @@index([projectId])
}
```

**Um pra um (1:1):** o lado com a FK precisa de `@unique`.

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

**Muitos pra muitos (N:N) implícita:** o Prisma cria a tabela de junção.

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

**`onDelete`:** `Cascade` (apaga os filhos), `Restrict` (bloqueia), `SetNull` (zera a FK, que precisa ser opcional), `NoAction`.

## 5. Client: CRUD

```ts
// criar
await prisma.project.create({ data: { name: 'App', description: 'Teste' } })
await prisma.project.createMany({ data: [{ name: 'A' }, { name: 'B' }], skipDuplicates: true })

// ler
await prisma.project.findMany()
await prisma.project.findUnique({ where: { id } })            // só campos @id/@unique
await prisma.project.findUniqueOrThrow({ where: { id } })     // lança P2025 se não achar
await prisma.project.findFirst({ where: { name: 'App' } })
await prisma.project.count()

// atualizar
await prisma.project.update({ where: { id }, data: { name: 'Novo' } })
await prisma.project.updateMany({ where: { status: 'ACTIVE' }, data: { status: 'ARCHIVED' } })

// criar ou atualizar
await prisma.project.upsert({
  where: { name: 'App' },
  update: { description: 'Atualizado' },
  create: { name: 'App', description: 'Novo' },
})

// apagar
await prisma.project.delete({ where: { id } })
await prisma.project.deleteMany({ where: { status: 'ARCHIVED' } })
```

`update` e `delete` lançam `P2025` se o registro não existir. `updateMany` e `deleteMany` devolvem `{ count }`.

## 6. Filtros (`where`)

```ts
where: {
  name: 'App',                                  // igual
  name: { contains: 'app', mode: 'insensitive' },
  name: { startsWith: 'A' },
  name: { endsWith: 'x' },
  name: { in: ['A', 'B'] },
  name: { not: 'C' },
  createdAt: { gte: new Date('2026-01-01'), lt: new Date('2027-01-01') },
  description: null,                            // IS NULL
  description: { not: null },
  AND: [{ status: 'ACTIVE' }, { name: { contains: 'a' } }],
  OR: [{ name: 'A' }, { name: 'B' }],
  NOT: { status: 'ARCHIVED' },
  tasks: { some: { title: 'x' } },              // relação: pelo menos um
  tasks: { every: { done: true } },             // todos
  tasks: { none: {} },                          // nenhum
}
```

## 7. Select, include e ordenação

```ts
// só alguns campos
await prisma.project.findMany({ select: { id: true, name: true } })

// trazer relações
await prisma.project.findUnique({
  where: { id },
  include: { tasks: true },
})

// relação filtrada e ordenada
await prisma.project.findMany({
  include: { tasks: { where: { done: false }, orderBy: { createdAt: 'desc' }, take: 5 } },
})

// ordenar
await prisma.project.findMany({ orderBy: [{ status: 'asc' }, { createdAt: 'desc' }] })
```

`select` e `include` não se misturam no mesmo nível. Use `select` com relações aninhadas dentro.

## 8. Paginação

```ts
// offset
await prisma.project.findMany({ skip: 20, take: 10 })

// cursor (melhor pra listas grandes)
await prisma.project.findMany({
  take: 10,
  skip: 1,
  cursor: { id: ultimoId },
  orderBy: { id: 'asc' },
})
```

## 9. Agregações

```ts
await prisma.task.aggregate({ _count: true, _avg: { points: true }, _max: { points: true } })

await prisma.task.groupBy({
  by: ['projectId'],
  _count: { _all: true },
  having: { projectId: { _count: { gt: 3 } } },
})
```

## 10. Escritas aninhadas

```ts
await prisma.project.create({
  data: {
    name: 'App',
    tasks: { create: [{ title: 'T1' }, { title: 'T2' }] },
  },
  include: { tasks: true },
})

// conectar a um registro existente
await prisma.task.create({
  data: { title: 'T3', project: { connect: { id: projectId } } },
})
```

Outras operações aninhadas: `connectOrCreate`, `disconnect`, `set`, `update`, `delete`.

## 11. Transações

```ts
// em lote: tudo ou nada
await prisma.$transaction([
  prisma.project.create({ data: { name: 'A' } }),
  prisma.task.deleteMany({ where: { done: true } }),
])

// interativa: usa o resultado de um passo no próximo
await prisma.$transaction(async (tx) => {
  const project = await tx.project.create({ data: { name: 'A' } })
  await tx.task.create({ data: { title: 'T1', projectId: project.id } })
})
```

Dentro da transação interativa, use `tx` e não `prisma`.

## 12. SQL cru

```ts
await prisma.$queryRaw`SELECT * FROM projects WHERE name = ${nome}`
await prisma.$executeRaw`UPDATE projects SET name = ${novo} WHERE id = ${id}`
```

Use sempre a tagged template (crase) pra parametrizar. `$queryRawUnsafe` com string concatenada abre brecha de SQL injection.

## 13. Integração com NestJS

**`prisma.service.ts`**

```ts
import { Injectable, OnModuleInit, OnModuleDestroy } from '@nestjs/common'
import { PrismaPg } from '@prisma/adapter-pg'
import { PrismaClient } from '../../generated/prisma/client'

@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit, OnModuleDestroy {
  constructor() {
    super({ adapter: new PrismaPg({ connectionString: process.env.DATABASE_URL }) })
  }

  async onModuleInit() { await this.$connect() }
  async onModuleDestroy() { await this.$disconnect() }
}
```

**`prisma.module.ts`**

```ts
@Global()
@Module({ providers: [PrismaService], exports: [PrismaService] })
export class PrismaModule {}
```

Importe o `PrismaModule` no `AppModule` e injete o `PrismaService` pelo construtor. Importe sempre como import normal, nunca `import type`, senão o Nest perde a classe em runtime.

**Tipos gerados:** `import { Project, Prisma } from '../generated/prisma/client'`. Use `Prisma.ProjectCreateInput`, `Prisma.ProjectWhereInput` etc. quando precisar tipar.

## 14. Códigos de erro comuns

- `P2002`: violação de unique (ex.: nome duplicado)
- `P2003`: violação de chave estrangeira
- `P2025`: registro não encontrado em update, delete ou `OrThrow`
- `P2021`: tabela não existe (migration não aplicada)
- `P1001`: não consegue alcançar o banco (container parado ou porta errada)
- `P1000`: falha de autenticação no banco

Tratamento no Nest:

```ts
import { Prisma } from '../generated/prisma/client'

try {
  await this.prisma.project.create({ data })
} catch (e) {
  if (e instanceof Prisma.PrismaClientKnownRequestError && e.code === 'P2002') {
    throw new ConflictException('Já existe um projeto com esse nome')
  }
  throw e
}
```

## 15. Seed

No `prisma.config.ts`, a chave `migrations.seed` define o comando:

```ts
export default defineConfig({
  schema: 'prisma/schema.prisma',
  datasource: { url: env('DATABASE_URL') },
  migrations: { seed: 'tsx prisma/seed.ts' },
})
```

Depois rode `pnpm prisma db seed`. O `migrate reset` também executa o seed.

## 16. Dev x produção

- **Dev:** `migrate dev` cria migrations e pode resetar o banco. Commite a pasta `prisma/migrations`.
- **Prod/CI:** apenas `migrate deploy`, que aplica o que já existe e nunca reseta.
- Nunca use `migrate reset` nem `db push` em produção.
- Use `DATABASE_URL` diferente por ambiente, com credenciais separadas.
- Rode `prisma generate` após cada `pnpm install` num clone novo (ou use `"postinstall": "prisma generate"`).
- Adicione `generated/` ao `.gitignore`.

## 17. Problemas frequentes

- **`Cannot find module '../../generated/prisma/client'`:** falta rodar `pnpm prisma generate`, ou o caminho do import não bate com o `output` do schema.
- **CLI e client em versões diferentes:** confira com `pnpm prisma -v` e fixe ambos na mesma major (`prisma@7` e `@prisma/client@7`).
- **`Drift detected` no migrate dev:** o banco tem tabelas que o histórico de migrations não explica. Em dev, `migrate reset` resolve.
- **Senha falhando com o container no ar:** pode haver outro Postgres na mesma porta (`netstat -ano | findstr :5432`). Mude a porta do container.
- **Validação do DTO não funciona:** falta `app.useGlobalPipes(new ValidationPipe())` ou o DTO foi importado com `import type`.
