
### Create Table
```sql
CREATE TABLE cursos (id ,nome ,aulas);
```

### Drop Table
```sql
DROP TABLE cursos;
```

### Definir Dados
```sqlite
CREATE TABLE cursos (
	id INTEGER NOT NULL,
	nome TEXT NOT NULL,
	aulas INTEGER
);
```

### Checar Tabela
```sqlite
PRAGMA TABLE_INFO('cursos'); 
```

### Aspas
- Aspas simples '' são usadas para strings e aspas duplas "" são usadas para identificadores dentro do sqlite, como nomes de colunas ou tabelas
- Podemos omitir aspas duplas
```sqlite
INSERT INTO "cursos" ("id", "nome", "aulas") VALUES (1, 'HTML', 10)
```