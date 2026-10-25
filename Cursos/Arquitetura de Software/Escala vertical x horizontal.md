
## Escala vertical (scale up)
É dar **mais poder à mesma máquina**: mais CPU, mais memória RAM, disco mais rápido.

- Exemplo: o servidor tem 4 GB de RAM e 2 vCPUs → você sobe para 32 GB e 8 vCPUs.
- **Vantagem:** simples. Não precisa mudar o código nem se preocupar com distribuição.
- **Limitações:** existe um teto físico (e financeiro), o custo cresce rápido nas máquinas maiores, e você continua com **ponto único de falha**: se aquela máquina cair, tudo cai. Muitas vezes também exige reiniciar o servidor para trocar a configuração.

## Escala horizontal (scale out)

É **adicionar mais máquinas (instâncias)** rodando a mesma aplicação, com um **load balancer** na frente distribuindo as requisições entre elas.

- Exemplo: em vez de um servidor grande, você sobe 5 instâncias menores da mesma aplicação.
- **Vantagem:** em teoria, o limite é muito maior, e você ganha **alta disponibilidade**: se uma instância cair, as outras continuam atendendo.
- **Desafios:** a aplicação precisa ser **stateless** (não guardar sessão ou estado na memória local, e sim em algo compartilhado como Redis ou o banco). Além disso, o **banco de dados vira o gargalo**, já que todas as instâncias apontam para o mesmo banco.

![[Pasted image 20261011184814.png]]

### Vertical na AWS: trocar o tipo da instância

Você continua com **uma única EC2**, mas muda o tipo dela para um maior.

```
Antes:   [EC2 t3.medium]   → 2 vCPU, 4 GB RAM
Depois:  [EC2 m5.2xlarge]  → 8 vCPU, 32 GB RAM
```

Como fazer: parar a instância, alterar o _instance type_ no console (ou via CLI/Terraform) e iniciar de novo. Isso gera **downtime**, mesmo que curto.

O mesmo vale para o banco: no **RDS**, você muda de `db.t3.medium` para `db.r5.2xlarge`. Também há uma janela de indisponibilidade (menor se usar Multi-AZ).

**Limite:** existe um maior tipo de instância disponível, e o preço sobe rápido. Se essa máquina cair, a aplicação inteira cai.

### Horizontal na AWS: mais instâncias atrás de um ALB

Você mantém o tipo da instância e **aumenta a quantidade**.

```
                      ┌→ [EC2 t3.medium #1]
Usuários → ALB ───────┼→ [EC2 t3.medium #2] → RDS
                      └→ [EC2 t3.medium #3]
```

Peças necessárias:

- **Launch Template / AMI**: a “receita” para criar instâncias idênticas.
- **Auto Scaling Group**: liga e desliga instâncias conforme métricas (ex.: CPU > 70%).
- **ALB**: distribui as requisições e faz _health check_, tirando do ar instâncias com problema.
- **Estado fora da instância**: sessões em ElastiCache (Redis), uploads em S3, dados no RDS.

Sem downtime: novas instâncias entram no ar enquanto as antigas continuam atendendo.