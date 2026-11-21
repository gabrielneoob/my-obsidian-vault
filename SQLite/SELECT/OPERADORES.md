Alguns operadores disponíveis são:

- `=`: Igual
    
- `!=`ou`<>`: Diferente
    
- `<`: Menor que
    
- `<=`: Menor ou igual a
    
- `>`: Maior que
    
- `>=`: Maior ou igual a
    

```sqlite
SELECT * FROM "produtos" WHERE "preco" < 50000;
SELECT * FROM "produtos" WHERE "lancamento" != 0;
SELECT * FROM "produtos" WHERE ("preco" + "taxa_importacao") < 40000;
SELECT * FROM "produtos" WHERE "id" = 3;
```

## Datas

O SQLite permite comparar datas diretamente, desde que estejam no formato correto (geralmente `YYYY-MM-DD` ou `YYYY-MM-DD HH:MM:SS`).

```sqlite
SELECT * FROM "produtos" WHERE "criado" > '2049';
SELECT * FROM "produtos" WHERE "criado" > '2049-08';

SELECT "nome", "criado" FROM "produtos" WHERE "criado" > '2049-08-03';
-- erro, ele vai ignorar -3. Tem que ser DD
SELECT "nome", "criado" FROM "produtos" WHERE "criado" > '2049-08-3';
```

## Textos

Em textos a comparação é sensível a maiúsculas e minúsculas, a menos que seja especificado o contrário com o `COLLATE NOCASE`.

```sqlite
SELECT * FROM "produtos" WHERE "nome" = 'Impressora 3D Mini';
SELECT * FROM "produtos" WHERE "nome" = 'ImpressorA 3D Mini'; -- não encontra
SELECT * FROM "produtos" WHERE "nome" = 'ImpressorA 3D Mini' COLLATE NOCASE;
```

## IS / IS NOT

O SQLite usa `IS` e `IS NOT` para verificar valores nulos e booleanos.

```sqlite
SELECT * FROM "produtos" WHERE "categoria" IS NULL;
SELECT * FROM "produtos" WHERE "categoria" IS NOT NULL;

SELECT * FROM "produtos" WHERE "lancamento" IS TRUE;
SELECT * FROM "produtos" WHERE "lancamento" IS FALSE;
```