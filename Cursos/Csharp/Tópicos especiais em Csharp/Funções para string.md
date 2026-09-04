• Formatar: ToLower(), ToUpper(), Trim()
• Buscar: IndexOf, LastIndexOf
• Recortar: Substring(inicio), Substring(inicio, tamanho)
• Substituir: Replace(char, char), Replace(string, string)
• String.IsNullOrEmpty(str), String.IsNullOrWhiteSpace(str)
• str.Split(' ')
• Conversãopara numero: intx = int.Parse(str), intx =Convert.ToInt32(str)
• Conversão de número: str= x.ToString(), str= x.ToString("C"), str= x.ToString("C3"), str= x.ToString("F2")

```c#
string original = "abcdeFGHIJ ABC abcDEFG ";
string s1 = original.ToUpper();
string s2 = original.ToLower(); 
string s3 = original.Trim(); 
intn1 = original.IndexOf("bc"); 
intn2 = original.LastIndexOf("bc"); 
string s4 = original.Substring(3); 
string s5 = original.Substring(3, 5); 
string s6 = original.Replace('a', 'x'); 
string s7 = original.Replace("abc", "xy"); 
boolb1 = String.IsNullOrEmpty(original); 
boolb2 = String.IsNullOrWhiteSpace(original); Console.WriteLine("Original: -" + original + "-"); Console.WriteLine("ToUpper: -"+ s1 + "-"); Console.WriteLine("ToLower: -"+ s2 + "-"); Console.WriteLine("Trim: -"+ s3 + "-"); Console.WriteLine("IndexOf('bc'): " + n1); Console.WriteLine("LastIndexOf('bc'): " + n2); Console.WriteLine("Substring(3): -" + s4 + "-"); Console.WriteLine("Substring(3, 5): -"+ s5 + "-"); Console.WriteLine("Replace('a', 'x'): -" + s6 + "-"); Console.WriteLine("Replace('abc', 'xy'): -" + s7 + "-"); Console.WriteLine("IsNullOrEmpty: " + b1); Console.WriteLine("IsNullOrWhiteSpace: " + b2);

```