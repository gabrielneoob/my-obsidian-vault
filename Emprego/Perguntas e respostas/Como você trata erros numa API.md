Uso o status HTTP para dizer quem errou: 4xx quando é erro de quem chamou, como 400 para dado inválido ou 404 para recurso inexistente, e 5xx para erro nosso. 

No Nest, eu lanço as exceptions prontas no service, como o NotFoundException, e o framework converte em resposta. 

Pra erro inesperado, o cliente recebe um 500 genérico, e o detalhe fica só no log, sem vazar informação interna. 

Um exception filter global padroniza o formato do erro e pode traduzir erros do banco, como uma violação de unicidade virando 409