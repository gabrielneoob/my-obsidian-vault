- Uma exceção é qualquer condição de erro ou comportamento inesperado encontrado por um programa *em execução*

- No .NET, uma exceção é um objeto herdado da classe System.Exception

- Quando lançada, uma exceção é propagada na pilha de chamadas de métodos em execução, até que seja capturada (tratada) ou o programa seja encerrado

![[Pasted image 20260914113954.png]]

- O modelo de tratamento de exceções permite que erros sejam tratados de forma consistente e flexível, usando boas práticas

- Vantagens:
	- Delega a lógica do erro para a classe / método responsável por conhecer as regras que podem ocasionar o erro
	- Trata de forma organizada (inclusive hierárquica) exceções de tipos diferentes
	- A exceção pode carregar dados quaisquer