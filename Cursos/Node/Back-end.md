## Server

Inicia um servidor que aceita conexões na porta
```js
const app = createServer((request, response) => {
  response.end("Servidor Funcionando");
});
app.listen(3000);
```

## Router
Permite o registro da rota e do handler(função executada quando a rota é acessada).

Handler
```js
function coursesHandler(request, response) {
  response.end("Cursos de Front End");
}
app.get("/cursos", coursesHandler);
```

Rota
```js
app.get("/cursos", (request, response) => {
  response.end("Cursos de Front End");
});
```
*Quando a pessoa acessar a rota de /cursos a função vai ser disparada*

## Request e Response
Receber dados da requisição e enviar uma resposta

```js
app.post("/criar/curso", (request, response) => {
  const { name, lessons } = request.body;
  db.createCourse(name, lessons);
  response.end("Curso Criado");
});
```

## Middleware
Executar funções antes de executar o handler.
```js
function auth(req) {
  return db.validateSession(req.cookie);
}

app.get(
  "/cursos",
  (req, res) => {
    res.end("Cursos de Front End");
  },
  [auth]
);
```

## Body Parse
Receber o corpo como uma stream e realizar o parse dele.
```js
async function bodyParser(req) {
  const chunks = [];
  for await (const chunk of req) {
    chunks.push(chunk);
  }
  const body = Buffer.concat(chunks).toString("utf-8");
  return JSON.parse(body);
}
```

## Banco de Dado
Conectar, ler e escrever em um banco de dados
```
const db = new Database("./db.sqlite");
db.prepare('SELECT * FROM "users" WHERE "id" = ?').get(1);
```

## Sessão
Criar e validar uma sessão
```js
app.post("/login", (req, res) => {
  const { email, password } = req.body;
  createSession(email, password);
  res.end("logged");
});

app.get("/session", (req, res) => {
  validateSession(req.cookies);
  res.end("valid");
});

```
