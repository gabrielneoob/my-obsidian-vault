**TTL** vem de _Time To Live_ (“tempo de vida”): é quanto tempo uma chave ainda vai existir no Redis antes de ser apagada automaticamente.
### Por que o `.ttl(key)` está no middleware

Ele pergunta ao Redis “quantos segundos faltam para essa chave expirar?”. Usamos a resposta no header `Retry-After`: se o TTL é 42, o cliente recebe `Retry-After: 42`, ou seja, “espere 42 segundos e tente de novo”.