- Deleta todas as linhas da tabela. Raramente é usado assim. geralmente usamos uma condicional
```sqlite
DELETE FROM "cursos";
```

- Neste exemplo vai deletar a linha na qual o id é igual a 1
```sqlite
DELETE FROM "cursos" WHERE "cursos".id = 1
```