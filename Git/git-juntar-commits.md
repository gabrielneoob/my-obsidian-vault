# Como juntar (squash) commits no Git

Guia rápido para transformar vários commits em um só, com os problemas mais comuns que aparecem no caminho.

> **Resumo:** para os últimos N commits, use `git reset --soft HEAD~N` + `git commit`, ou `git rebase -i HEAD~N` trocando `pick` por `squash`. Se já deu push, finalize com `git push --force-with-lease`.

---

## Quando faz sentido

- Commits de "ajuste", "fix typo" ou "esqueci um arquivo" que pertencem à mesma mudança.
- Deixar o histórico da branch limpo antes de abrir um Pull Request.

**Evite** reescrever histórico em branches compartilhadas (`main`, `develop`) ou que outras pessoas já usam.

---

## Antes de começar

```bash
git status            # árvore de trabalho limpa?
git log --oneline -5  # confirme quais commits serão juntados
```

---

## Opção 1: `reset --soft` (mais simples)

Junta os **N últimos** commits. Exemplo com 2:

```bash
git reset --soft HEAD~2
git commit -m "feat: mensagem final do commit"
```

O `HEAD~2` volta dois commits, mas mantém todas as alterações na área de staging. Depois é só criar um único commit.

**Limitação:** só funciona bem para commits consecutivos no topo da branch.

---

## Opção 2: rebase interativo (mais flexível)

```bash
git rebase -i HEAD~2
```

O Git abre o editor (normalmente o Vim) com algo assim:

```
pick a1b2c3d feat: docker compose yml
pick e4f5g6h fix .env-example
```

Troque o `pick` do **segundo** commit por `squash` (ou `s`):

```
pick a1b2c3d feat: docker compose yml
squash e4f5g6h fix .env-example
```

Salve e feche. O Git abre outro editor para a mensagem final do commit combinado. Ajuste, salve e feche de novo.

### `squash` x `fixup`

| Comando | O que faz com a mensagem |
|---|---|
| `squash` (`s`) | Junta o commit ao anterior e deixa você **editar** a mensagem combinada |
| `fixup` (`f`) | Junta o commit ao anterior e **descarta** a mensagem dele |

### Regra de ouro

O commit que fica no topo da lista (o mais antigo) deve continuar como `pick`. Os que você quer absorver recebem `squash`/`fixup`, sempre **abaixo** do commit que vai recebê-los.

---

## Salvando e saindo do Vim

Para editar o texto, aperte `i`. Quando terminar, aperte `Esc` e use um dos comandos:

| Comando | O que faz |
|---|---|
| `:wq` + `Enter` | Salva e sai |
| `:x` + `Enter` | Salva e sai (só grava se houve mudança) |
| `ZZ` | Atalho para salvar e sair |
| `:q!` + `Enter` | Sai **sem salvar** (cancela a edição) |

Para usar outro editor no Git (exemplo: VS Code):

```bash
git config --global core.editor "code --wait"
```

---

## Terminando o rebase

Enquanto o rebase não termina, o prompt mostra algo como `(minha-branch|REBASE 2/2)` e você está em *detached HEAD*. Nesse estado, `git push` **falha** com:

```
fatal: You are not currently on a branch.
```

Para encerrar:

```bash
git status              # veja se há conflitos
git add .               # só se houver conflitos já resolvidos
git rebase --continue   # finaliza
```

Quando terminar, o prompt volta a mostrar apenas `(minha-branch)`.

Nem sempre é preciso rodar `git commit --amend` durante o rebase: a mensagem já é editada na etapa do `squash`. Se rodar, o rebase continua pendente e você ainda precisa do `git rebase --continue`.

Para desistir e voltar ao estado de antes:

```bash
git rebase --abort
```

---

## Conferindo o resultado

```bash
git log --oneline -5      # os commits devem aparecer como um só
git show --stat HEAD      # quais arquivos entraram no commit
```

**Importante:** confirme que arquivos sensíveis (como o `.env` real) **não** aparecem na lista. Apenas o `.env.example`, sem valores reais, deve ser versionado.

---

## Enviando para o remoto

Se os commits **ainda não** tinham sido enviados:

```bash
git push -u origin minha-branch
```

Se **já tinham** sido enviados, o histórico foi reescrito (os hashes mudaram) e o push normal será rejeitado:

```bash
git push --force-with-lease
```

Prefira `--force-with-lease` ao `--force`: ele recusa o push se alguém tiver enviado commits novos na branch nesse meio tempo, evitando sobrescrever o trabalho dos outros.

---

## Se algo der errado

O `reflog` guarda o histórico de movimentos do `HEAD`, e permite voltar a qualquer estado anterior:

```bash
git reflog
git reset --hard <hash-de-antes-do-squash>
```

---

## Resumo dos comandos

| Objetivo | Comando |
|---|---|
| Juntar os 2 últimos commits (simples) | `git reset --soft HEAD~2` + `git commit` |
| Juntar com rebase interativo | `git rebase -i HEAD~2` |
| Continuar o rebase | `git rebase --continue` |
| Cancelar o rebase | `git rebase --abort` |
| Enviar após reescrever histórico | `git push --force-with-lease` |
| Recuperar estado anterior | `git reflog` + `git reset --hard <hash>` |
