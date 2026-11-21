### Front-end (React/Next.js)

**1. Code splitting com import dinâmico:** carrega o componente pesado só quando é preciso.

tsx

```tsx
import dynamic from 'next/dynamic';

const Chart = dynamic(() => import('./Chart'), {
  ssr: false,
  loading: () => <p>Carregando gráfico...</p>,
});
```

**2. Imagens otimizadas:** o `next/image` serve WebP/AVIF, faz lazy loading e evita layout shift.

tsx

```tsx
import Image from 'next/image';

<Image src="/banner.jpg" alt="Banner" width={1200} height={600} priority />
```

**3. Evitar re-renders desnecessários:**

tsx

```tsx
const total = useMemo(() => items.reduce((acc, i) => acc + i.price, 0), [items]);

const handleSelect = useCallback((id: string) => setSelected(id), []);

const Row = memo(function Row({ item }: { item: Item }) {
  return <li>{item.name}</li>;
});
```

**4. Debounce em buscas:** evita uma requisição por tecla digitada.

tsx

```tsx
const [query, setQuery] = useState('');

useEffect(() => {
  const timer = setTimeout(() => fetchResults(query), 400);
  return () => clearTimeout(timer);
}, [query]);
```

**5. Virtualização de listas grandes:** renderiza só o que aparece na tela (`@tanstack/react-virtual` ou `react-window`).

**6. Cache e renderização no Next:** páginas estáticas com revalidação (ISR).

tsx

```tsx
export const revalidate = 60; // regenera a página no máximo a cada 60s
```

### Back-end (NestJS + Prisma + PostgreSQL)

**1. Evitar N+1:** buscar relações em uma query só, em vez de uma por item.


```ts
// Ruim: 1 query + N queries
const projects = await prisma.project.findMany();
for (const p of projects) {
  p.tasks = await prisma.task.findMany({ where: { projectId: p.id } });
}

// Bom: resolve com JOIN/IN
const projects = await prisma.project.findMany({
  include: { tasks: true },
});
```

**2. Selecionar só os campos necessários:**


```ts
const users = await prisma.user.findMany({
  select: { id: true, name: true, email: true },
});
```

**3. Paginação por cursor:** o `OFFSET` fica lento em tabelas grandes.

ts

```ts
const items = await prisma.task.findMany({
  take: 20,
  skip: cursor ? 1 : 0,
  cursor: cursor ? { id: cursor } : undefined,
  orderBy: { id: 'asc' },
});
```

**4. Índices no schema:** colunas usadas em `WHERE`, `JOIN` e `ORDER BY`.

```prisma
model Task {
  id        String @id @default(uuid())
  projectId String
  status    String

  @@index([projectId, status])
}
```

**5. Cache com Redis:** a URL e as credenciais ficam no `.env`, nunca no código.


```ts
// .env
// REDIS_URL=redis://localhost:6379

@Injectable()
export class ProjectsService {
  constructor(
    @Inject(CACHE_MANAGER) private cache: Cache,
    private prisma: PrismaService,
  ) {}

  async findAll() {
    const cached = await this.cache.get<Project[]>('projects:all');
    if (cached) return cached;

    const projects = await this.prisma.project.findMany();
    await this.cache.set('projects:all', projects, 60_000); // TTL 60s
    return projects;
  }
}
```

**6. Paralelizar chamadas independentes:**

ts

```ts
// Sequencial: soma os tempos
const user = await this.usersService.find(id);
const orders = await this.ordersService.findByUser(id);

// Paralelo: leva o tempo da mais lenta
const [user, orders] = await Promise.all([
  this.usersService.find(id),
  this.ordersService.findByUser(id),
]);
```

**7. Tirar trabalho pesado da requisição:** envio de e-mail, geração de PDF e processamentos longos vão para uma fila (RabbitMQ, BullMQ). A API responde rápido e o worker processa em segundo plano.

**8. Compressão das respostas:**

ts

```ts
import compression from 'compression';
app.use(compression());
```

---

### Como medir antes de otimizar

- **Front:** Lighthouse, React DevTools Profiler e Web Vitals (LCP, INP, CLS).
- **Back:** `EXPLAIN ANALYZE` no PostgreSQL, logs de query do Prisma (`log: ['query']`) e métricas de latência p95/p99.