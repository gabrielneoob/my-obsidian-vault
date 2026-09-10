- override
- virtual

Para um método de uma superclasse ser sobrescrito(override), o método precisa permitir com a sobreposição com o virtual

Account
```c#
public virtual void Withdraw(double amount)
{
    this.Balance -= amount + 5.0;
}
```

SavingsAccount : Account
```c#
        public sealed override void Withdraw(double amount)
        {
            base.Withdraw(amount);
            this.Balance -= 2.0;
        }
```
*sealed não deixa o método de uma subclasse ser sobrescrito*