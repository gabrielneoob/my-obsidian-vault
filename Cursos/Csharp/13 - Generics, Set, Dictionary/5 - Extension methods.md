- São métodos que estendem a funcionalidade de um tipo, sem precisar alterar o código fonte deste tipo, nem herdar desse tipo

- Como fazer um extension method?
	- Criar uma classe estática
	- Na classe, criar um método estático
	- O primeiro parâmetro do método deverá ter o prefixo **this**, seguida da declaração de um parâmetro do tipo que se deseja estender. Esta será uma referência para o próprio objeto.

```c#
using System.Globalization;

  

namespace Course.Extensions

{

  static class DateTimeExtensions

  {

    public static string ElapsedTime(this DateTime thisObj)

    {

      TimeSpan duration = DateTime.Now.Subtract(thisObj);

  

      if (duration.TotalHours < 24.0)

      {

        return duration.TotalHours.ToString("F1", CultureInfo.InstalledUICulture) + " hours";

      }

      else

      {

        return duration.TotalDays.ToString("F1", CultureInfo.InvariantCulture) + " days";

      }

    }

  }

}
```