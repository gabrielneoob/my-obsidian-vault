```c#
namespace Course
{
    internal class ExercicioWhile1
    {
        static public void Executar()
        {
            int num = int.Parse(Console.ReadLine());
            int alcool = 0;
            int gasolina = 0;
            int diesel = 0;

            while(num != 4)
            {
                num = int.Parse(Console.ReadLine());
                switch(num)
                {
                    case 1:
                        alcool += 1;
                        break;
                    case 2:
                        gasolina += 1;
                        break;
                    case 3:
                        diesel += 1;
                        break;
                }
            }

            Console.WriteLine("MUITO OBRIGADO");
            Console.WriteLine($"Alcool {alcool}");
            Console.WriteLine($"Gasolina {gasolina}");
            Console.WriteLine($"diesel {diesel}");
        }
    }
}
```
