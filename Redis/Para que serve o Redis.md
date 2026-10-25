Redis é um banco de dados **em memória** (RAM), do tipo chave-valor. Em vez de guardar tudo em disco como o Postgres, ele mantém os dados na memória, então leitura e escrita levam microssegundos.

- Redis guarda os dados na **RAM** da maquina onde ele está rodando
- O recurso que mais importa aqui é o **TTL** (time to live): você grava uma chave com prazo de validade e o Redis apaga sozinho quando expira. Isso se encaixa muito bem em dados temporários.
## Casos de uso
1. **Rate limiting**: contar requisições por IP/usuário numa janela de tempo.
2. **Cache**: guardar o resultado de consultas pesadas para não bater no banco toda hora.
3. **Sessões e tokens**: por exemplo, blacklist de access tokens revogados.
4. **Filas e pub/sub**: BullMQ, por exemplo, usa Redis por baixo.
5. **Locks distribuídos e contadores**.