- Seleciona as colunas selecionadas
```sqlite
SELECT * FROM "cursos";
```

```sqlite
SELECT "id", "nome" FROM "cursos";
```

### Limit
- Limita o numero de linhas retornadas pela consulta.
```sqlite
SELECT "id", "nome" FROM "cursos" LIMIT 10;
```

### Where
- Filtra as linhas da tabela com base na condição passada
```sqlite
SELECT "id", "nome" FROM "cursos" WHERE "id" = 1
```

### AND e OR
- **AND** todas as condições devem ser verdadeiras. **OR** pelo menos uma das condições deve ser verdadeira
```sqlite
SELECT "id", "nome" FROM "cursos" WHERE "id" = 1 AND "aulas" > 10;

SELECT "id", "nome" FROM "cursos" WHERE "id" = 1 OR "aulas" > 10;
```
