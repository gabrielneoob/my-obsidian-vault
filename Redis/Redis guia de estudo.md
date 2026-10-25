# Redis: guia de estudo

Guia prático de Redis aplicado ao projeto users-system (Express, Node, Prisma e Postgres).

## 1. O que é o Redis

Redis (Remote Dictionary Server) é um banco de dados em memória do tipo chave-valor. Os dados ficam na RAM, então leitura e escrita levam microssegundos. Ele não tem tabelas, joins nem schema: você guarda um valor sob uma chave e busca por ela.

Não substitui o Postgres. Os dois têm papéis diferentes e costumam trabalhar juntos.

## 2. Redis x Postgres

|  | Postgres | Redis |
| --- | --- | --- |
| Armazenamento | Disco (durável) | RAM (rápido, volátil por padrão) |
| Modelo | Tabelas relacionais | Chave-valor e estruturas de dados |
| Consulta | SQL, filtros, joins | Acesso por chave |
| Uso ideal | Dados que não podem se perder (usuários, refresh tokens) | Dados temporários ou acessados com muita frequência (contadores, cache) |
| Capacidade | Limitada pelo disco | Limitada pela RAM |

No users-system, usuários e refresh tokens ficam no Postgres, e o contador do rate limit fica no Redis.

## 3. Casos de uso

- **Rate limiting:** contar requisições por IP ou usuário numa janela de tempo.
- **Cache:** guardar o resultado de consultas pesadas para não bater no banco toda hora.
- **Dados temporários:** códigos de verificação, tokens de reset de senha, blacklist de access tokens revogados.
- **Filas e jobs:** bibliotecas como BullMQ usam Redis por baixo.
- **Pub/Sub e Streams:** troca de mensagens entre processos.
- **Locks distribuídos e contadores:** coordenar várias instâncias da API.
- **Rankings:** sorted sets mantêm itens ordenados por pontuação.

## 4. Como funciona por dentro

- **Processo separado:** o Redis não roda dentro do app Node. O Node conversa com ele pela rede (no projeto, via ioredis). Se a API reiniciar, os dados continuam lá.
- **Memória do servidor do Redis:** no ambiente local, é a RAM usada pelo container users-system-redis. Em produção, é a RAM da instância (por exemplo, um ElastiCache na AWS).
- **Comandos atômicos:** a execução dos comandos acontece em uma única thread, então cada comando roda por inteiro sem ser interrompido por outro. É isso que torna o INCR seguro mesmo com milhares de requisições simultâneas.
- **Persistência opcional:** o Redis pode gravar em disco. O **RDB** tira snapshots periódicos da memória. O **AOF** registra cada escrita num arquivo para reaplicar depois. No compose, o volume redisdata:/data é onde esses arquivos ficam.
- **Limite de memória:** a configuração maxmemory define o teto de uso, e maxmemory-policy decide o que apagar ao chegar nele (por exemplo, as chaves menos usadas, no caso de um cache).

## 5. Tipos de dados

| Tipo | O que é | Exemplo de uso |
| --- | --- | --- |
| String | Texto, número ou bytes | Contador de rate limit, cache de um JSON |
| Hash | Mapa de campos e valores | Dados de uma sessão ou de um usuário |
| List | Lista ordenada por inserção | Filas simples |
| Set | Conjunto sem repetição | Tags, IDs únicos |
| Sorted Set | Conjunto ordenado por pontuação | Rankings, rate limit com janela deslizante |
| Stream | Log de eventos com consumidores | Mensageria |

No rate limit do projeto usamos só String (o contador).

## 6. Comandos essenciais

Abra o CLI com `docker compose exec redis redis-cli`.

```
SET nome Gabriel          # grava
GET nome                  # lê
DEL nome                  # apaga
EXISTS nome               # 1 se existe, 0 se não

SET sessao abc123 EX 60   # grava com expiração de 60 segundos
TTL sessao                # quantos segundos faltam
EXPIRE chave 30           # define expiração de uma chave existente

INCR contador             # soma 1 (cria com 1 se não existir)

HSET user:1 name Gabriel role ADMIN
HGETALL user:1

KEYS rate-limit:*         # lista chaves (só em desenvolvimento)
SCAN 0 MATCH rate-limit:* COUNT 100   # forma segura para produção
```

O CLI do compose já autentica sozinho, porque o container tem a variável REDISCLI\_AUTH.

## 7. TTL em detalhe

TTL (Time To Live) é o tempo que uma chave ainda vai existir antes de o Redis apagá-la sozinho.

- **EXPIRE chave 60:** define o TTL. Responde 1 se definiu e 0 se não definiu.
- **TTL chave:** consulta quantos segundos faltam.
- **PTTL chave:** o mesmo, em milissegundos.
- **EXPIRE chave 60 NX:** só define o TTL se a chave ainda não tiver um (disponível a partir do Redis 7).

Valores especiais do TTL:

- `-1`: a chave existe mas não tem expiração.
- `-2`: a chave não existe.

O TTL também protege a memória: sem expiração, chaves de dados temporários ficariam ocupando RAM para sempre.

## 8. Infraestrutura no projeto

### docker-compose.yml

```yaml
  redis:
    image: redis:7-alpine
    container_name: users-system-redis
    restart: unless-stopped
    command: ['redis-server', '--requirepass', '${REDIS_PASSWORD}']
    environment:
      REDISCLI_AUTH: ${REDIS_PASSWORD}
    ports:
      - '127.0.0.1:${REDIS_PORT}:6379'
    volumes:
      - redisdata:/data
    healthcheck:
      test: ['CMD-SHELL', 'redis-cli ping | grep PONG']
      interval: 5s
      timeout: 3s
      retries: 5
```

Pontos importantes:

- **--requirepass:** exige senha. Redis sem senha exposto é uma falha de segurança clássica.
- **127.0.0.1 na porta:** só a própria máquina acessa.
- **REDISCLI\_AUTH:** permite rodar redis-cli sem digitar a senha, inclusive no healthcheck.
- **Indentação:** redis e postgres precisam estar no mesmo nível dentro de services.

### Variáveis de ambiente (.env.example)

```
REDIS_PASSWORD=troque-esta-senha
REDIS_PORT=6379
REDIS_URL=redis://:troque-esta-senha@localhost:6379
```

O formato da URL é `redis://:SENHA@host:porta`. Os dois pontos antes da senha existem porque o Redis não tem usuário por padrão. A senha real fica só no .env, que não é versionado. O código nunca conhece a senha, só lê REDIS\_URL.

### Cliente em src/shared/redis.ts

```ts
import { Redis } from 'ioredis'

const redisUrl = process.env['REDIS_URL']

if (!redisUrl) {
  throw new Error('REDIS_URL não definida')
}

export const redis = new Redis(redisUrl)

redis.on('error', (err) => {
  console.error('[redis] erro de conexão:', err.message)
})
```

- **Falha cedo:** sem REDIS\_URL, o app nem sobe.
- **Uma conexão só:** o módulo é carregado uma vez, então todo import recebe a mesma instância (singleton). Abrir uma conexão por requisição seria um erro grave de desempenho.
- **Reconexão automática:** o ioredis reconecta sozinho se a conexão cair.
- **Listener de error:** sem ele, falhas de conexão viram eventos sem tratamento.

## 9. Rate limit por IP

### A ideia (janela fixa)

Para cada IP existe uma chave, por exemplo `rate-limit:auth:200.1.2.3`.

1. Toda requisição faz INCR na chave, que devolve o contador atual.
2. Na primeira requisição, a chave ganha um TTL igual à janela (por exemplo, 60 segundos).
3. Quando o TTL expira, o Redis apaga a chave e o contador recomeça do zero.
4. Se o contador passar do máximo, a API responde 429 Too Many Requests.

Por que Redis e não um Map em memória do Node: o Map some quando o processo reinicia, e com várias instâncias da API cada uma teria o próprio contador, o que permitiria burlar o limite. O Redis é o estado compartilhado entre elas.

### Parâmetros

- **keyPrefix:** separa os contadores por finalidade (global, auth).
- **windowInSeconds:** duração da janela. É usado no EXPIRE.
- **maxRequests:** quantas requisições são permitidas dentro da janela.

| Cenário | windowInSeconds | maxRequests |
| --- | --- | --- |
| Limite global da API | 60 | 100 |
| Login (anti força bruta) | 900 | 10 |
| Endpoint caro | 3600 | 20 |

### Middleware (src/shared/middlewares/rate-limit.ts)

```ts
import type { RequestHandler } from 'express'
import { redis } from '../redis.js'
import { TooManyRequestsError } from '../errors/app-error.js'

type RateLimitOptions = {
  keyPrefix: string
  windowInSeconds: number
  maxRequests: number
}

export const rateLimit =
  ({
    keyPrefix,
    windowInSeconds,
    maxRequests,
  }: RateLimitOptions): RequestHandler =>
  async (req, res, next) => {
    const key = `rate-limit:${keyPrefix}:${req.ip}`

    let count: number
    let ttl: number

    try {
      const results = await redis
        .multi()
        .incr(key)
        .expire(key, windowInSeconds, 'NX')
        .ttl(key)
        .exec()

      const [incrResult, , ttlResult] = results ?? []

      if (!incrResult || incrResult[0] || !ttlResult || ttlResult[0]) {
        throw new Error('Falha ao executar o rate limit no Redis')
      }

      count = incrResult[1] as number
      ttl = ttlResult[1] as number
    } catch (err) {
      console.error('[rate-limit]', err)
      next()
      return
    }

    res.setHeader('X-RateLimit-Limit', maxRequests)
    res.setHeader('X-RateLimit-Remaining', Math.max(maxRequests - count, 0))

    if (count > maxRequests) {
      res.setHeader('Retry-After', Math.max(ttl, 1))
      throw new TooManyRequestsError()
    }

    next()
  }
```

### Decisões de projeto

- **MULTI:** INCR, EXPIRE e TTL rodam em bloco. Se fossem comandos soltos, o processo poderia cair entre o INCR e o EXPIRE e deixar uma chave sem expiração, bloqueando aquele IP para sempre.
- **EXPIRE com NX:** a primeira requisição abre a janela e as seguintes não a estendem.
- **Ordem dos resultados:** o exec() devolve um resultado por comando, na ordem encadeada. Índice 0 é o INCR, índice 1 é o EXPIRE (1 ou 0) e índice 2 é o TTL. Por isso a desestruturação pula o do meio com a vírgula dupla.
- **Retry-After:** vem do comando TTL e diz ao cliente quantos segundos esperar.
- **Fail open:** se o Redis cair, a requisição é liberada e o erro é logado. Em endpoints muito sensíveis, há quem prefira fail closed (bloquear).
- **Erros no formato da API:** o TooManyRequestsError estende AppError (status 429), então o errorHandler responde com `{ error: { code, message } }`.
- **req.ip:** atrás de proxy ou load balancer (Cloudflare, Nginx, AWS) é preciso configurar `app.set('trust proxy', ...)`, senão todos os clientes aparecem com o IP do proxy e compartilham o mesmo contador.

### Como aplicar

No app.ts, um limite global depois do /health (para o health check não consumir cota):

```ts
app.use(rateLimit({ keyPrefix: 'global', windowInSeconds: 60, maxRequests: 100 }))
```

Nas rotas de credenciais, um limite mais restrito antes do validate (assim requisições inválidas também contam):

```ts
const authRateLimit = rateLimit({
  keyPrefix: 'auth',
  windowInSeconds: 15 * 60,
  maxRequests: 10,
})

authRouter.post('/signin', authRateLimit, validate(signInSchema), authController.signIn)
```

Com os limites global e de auth ativos, cada requisição passa pelos dois, e cada um conta na própria chave.

### Limitação da janela fixa

Quem manda 5 requisições no último segundo de uma janela e mais 5 no primeiro segundo da próxima consegue 10 em 2 segundos, o dobro do limite. As alternativas são a janela deslizante (sliding window, geralmente com sorted set) e o token bucket. As bibliotecas express-rate-limit e rate-limit-redis cobrem esses casos.

## 10. Boas práticas

- **Prefixe as chaves** por finalidade: `rate-limit:auth:IP`, `cache:users:ID`. Facilita buscar, limpar e depurar.
- **Sempre defina TTL** em dados temporários.
- **Use uma única conexão** compartilhada.
- **Prefira SCAN a KEYS** em produção, porque KEYS varre tudo e bloqueia o Redis.
- **Guarde valores pequenos.** Redis é para dados quentes, não para arquivos grandes.
- **Não use o Redis como única fonte da verdade** de dados importantes. Se o dado não pode se perder, o lugar dele é o Postgres.
- **Defina maxmemory** em produção, com uma política de remoção adequada ao uso.
- **Decida a política de falha** (fail open ou fail closed) antes de colocar o Redis no caminho de requisições críticas.

## 11. Segurança

- Sempre exigir senha (requirepass).
- Expor a porta só em 127.0.0.1 localmente, e em produção só dentro de rede privada.
- Senha e URL de conexão ficam no .env, nunca no código nem em arquivos versionados.
- Se a senha tiver caracteres especiais (`@`, `/`, `#`), use senha alfanumérica ou faça URL-encode na REDIS\_URL.
- Nunca deixe uma instância de Redis sem senha acessível pela internet.

## 12. Erros comuns

- **YAML mal indentado** no compose, deixando o redis dentro do postgres.
- **Confundir os índices do exec():** ler o resultado do EXPIRE (0 ou 1) achando que é o TTL.
- **EXPIRE e TTL são comandos diferentes:** um define, o outro consulta.
- **INCR sem EXPIRE:** a chave nunca expira.
- **req.ip atrás de proxy** sem trust proxy configurado.
- **Esquecer o REDIS\_PASSWORD no .env**, fazendo o Redis subir com requirepass vazio.
- **Logs de debug no middleware** em produção, a cada requisição.

## 13. Próximos passos

- Trocar o middleware manual por express-rate-limit com rate-limit-redis e comparar as duas versões.
- **Cache (cache-aside):** buscar no Redis, se não achar buscar no Postgres, gravar no Redis com TTL e devolver. Bom candidato: GET /users/:id.
- **Blacklist de access tokens** revogados, com TTL igual ao tempo restante do JWT.
- **Filas:** BullMQ usa Redis. O roteiro do projeto prevê mensageria para as notificações, então vale comparar as opções quando chegar lá.
- **Pub/Sub e Streams** para eventos entre serviços.

## 14. Glossário

- **Chave-valor:** modelo em que cada dado é guardado sob uma chave única.
- **TTL:** tempo de vida restante de uma chave.
- **Atômico:** operação que acontece inteira ou não acontece, sem ser interrompida.
- **MULTI/EXEC:** bloco de comandos executados em sequência, sem outros comandos no meio.
- **RDB:** snapshot periódico da memória gravado em disco.
- **AOF:** arquivo que registra cada escrita para reaplicar depois.
- **Singleton:** instância única compartilhada pela aplicação.
- **Fail open / fail closed:** liberar ou bloquear requisições quando o serviço de apoio falha.
- **Janela fixa:** período de contagem que começa na primeira requisição e zera ao expirar.
- **Sliding window:** janela que acompanha o tempo, evitando rajadas na virada da janela fixa.
