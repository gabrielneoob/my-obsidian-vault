- Representa um INSTANTE
- É um tipo valor (struct)

## Representação Interna

- Um objeto DateTime internamente armazena:
	- O número de "ticks" (100 nanosegundos) desde a meia noite do dia 1 de janeiro do ano 1 da era comum

## Instanciação

- Construtores
	- DateTime(ano, mes, dia)
	- DateTime(ano, mes, dia, hora, minuto, segundo) *opcional*
	- DateTime(ano, mes, dia, hora, minuto, segundo, milisegundos) *opcional*

- Builders
	- DateTime.New
	- DateTime.UtcNow
	- DateTime.Today
	- DateTime.Parse(string)
	- DateTime.ParseExact(string, string)

## Propriedades
- Date (DateTime)
- Day (int)
- DayOfWeek (DayOfWeek)
- DayOfYear (int)
- Hour (int)
- Kind (DateTimeKind)
- Millisecond (int)
- minute (int)
- Month (int)
- Second (int)
- Ticsk (long)
- TimeOfDay (TimeSpan)
- Year (int)

```c#
namespace Course
{
    class Program
    {
        static public void Main()
        {
            DateTime d = new DateTime(2001, 8, 15, 13, 45, 58, 275);

            Console.WriteLine(d);
            Console.WriteLine("1) Date: " + d.Date);
            Console.WriteLine("2) Day: " + d.Day);
            Console.WriteLine("3) Month: " + d.Month);
            Console.WriteLine("4) Year: " + d.Year);
            Console.WriteLine("5) DayOfWeek: " + d.DayOfWeek);
            Console.WriteLine("6) DayOfYear: " + d.DayOfYear);
            Console.WriteLine("7) TimeOfDay: " + d.TimeOfDay);

        }
    }
}
```

## Operações com DateTime

```c#
DateTime x = DateTime.Now;

DateTime y = x.Add(timeSpan);
DateTime y = x.AddDays(double);
DateTime y = x.AddHours(double);
DateTime y = x.AddMilliseconds(double);
DateTime y = x.AddMinutes(double);
DateTime y = x.AddMonths(int);
DateTime y = x.AddSeconds(double);
DateTime y = x.AddTicks(long);
DateTime y = x.AddYears(int);

DateTime y = x.Subtract(timeSpan);
TimeSpan t = x.Subtract(dateTime);
```