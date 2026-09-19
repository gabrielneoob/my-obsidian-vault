- Bloco try
	- Contém o código que representa a execução normal do trecho de código que **pode** acarretar em uma exceção

- Bloco **catch**
	- Contém o código a ser executado caso uma exceção ocorra
	- Deve ser especificado o tipo de exceção a ser tratada (upcasting é permitido)

```c#
namespace Course

{

  class Program

  {

    static void Main(string[] args)

    {

      try

      {

        int n1 = int.Parse(Console.ReadLine());

        int n2 = int.Parse(Console.ReadLine());

  

        int result = n1 / n2;

  

        System.Console.WriteLine(result);

      }

      catch (DivideByZeroException)

      {

        System.Console.WriteLine("Division by zero is not allowed! ");

      }

      catch (FormatException e)

      {

        System.Console.WriteLine("Format Error! " + e.Message);

      }

  

    }

  }

}
```