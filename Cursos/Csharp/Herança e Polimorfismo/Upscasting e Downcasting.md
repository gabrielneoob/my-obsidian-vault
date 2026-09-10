- Upcasting
	- Casting da subclasse para superclasse
	- Uso comum: polimorfismo

- Downcasting
	- Casting da superclasse para subclasse
	- Palavra as
	- Palavra is
	- Uso comum: métodos que recevem parâmetros genéricos(ex: Equals)

```c#
            Account acc = new Account(1001, "Alex", 0.0);
            BusinessAccount bacc = new BusinessAccount(1002, "Maria", 0, 500.00);

            // UPCASTING

            Account acc1 = bacc;
            Account acc2 = new BusinessAccount(1003, "Bob", 0.0, 200.0);
            Account acc3 = new SavingsAccount(1004, "Anna", 0.0, 0.01);

            // ERROR = acc2.Loan();

            // DOWNCASTING

            BusinessAccount acc4 = acc2 as BusinessAccount;
            acc4.Loan(100.00);

            // ERROR = BusinessAccount acc5 = as acc3;

            if( acc3 is BusinessAccount)
            {
                BusinessAccount acc5 = acc3 as BusinessAccount;
                acc5.Loan(200.00);
                Console.WriteLine("Loan!");
            }

            if (acc3 is SavingsAccount)
            {
                SavingsAccount acc5 = acc3 as SavingsAccount;
                acc5.UpdateBalance();
                Console.WriteLine("Update!");
            }

```
