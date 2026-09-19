# Cheatsheet — dotnet CLI

## Instalação do SDK

### Linux (script oficial — funciona na maioria das distros)
```bash
curl -sSL https://dot.net/v1/dotnet-install.sh | bash /dev/stdin --channel LTS
```
Depois, adicione ao `PATH` (ex: no `~/.bashrc` ou `~/.zshrc`):
```bash
export DOTNET_ROOT=$HOME/.dotnet
export PATH=$PATH:$DOTNET_ROOT:$DOTNET_ROOT/tools
```

### Linux via gerenciador de pacotes
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install dotnet-sdk-8.0

# Fedora
sudo dnf install dotnet-sdk-8.0

# Arch
sudo pacman -S dotnet-sdk
```

### macOS
```bash
brew install dotnet
```
Ou baixando o instalador `.pkg` em https://dotnet.microsoft.com/download

### Windows
Baixe o instalador em https://dotnet.microsoft.com/download ou, via `winget`:
```powershell
winget install Microsoft.DotNet.SDK.8
```

### Conferir instalação
```bash
dotnet --version
dotnet --list-sdks
```

> Dica: o site oficial (https://dotnet.microsoft.com/download) sempre tem os instaladores mais atualizados para cada SO e versão do SDK (LTS vs mais recente).

## Criar projeto
```bash
dotnet new console -o NomeDoProjeto     # cria um projeto de console
dotnet new classlib -o NomeDaLib        # biblioteca de classes
dotnet new sln -o NomeDaSolution        # cria uma solution
dotnet new gitignore                    # gera um .gitignore padrão .NET
```

## Build e execução
```bash
dotnet build                # compila (procura .csproj/.sln na pasta atual)
dotnet build NomeProjeto    # compila um projeto específico
dotnet run                  # compila e executa
dotnet run --project Pasta  # roda um projeto específico sem entrar na pasta
dotnet watch run            # roda e recompila automaticamente a cada save
```

## Restaurar e limpar
```bash
dotnet restore   # baixa os pacotes NuGet do projeto
dotnet clean     # limpa os artefatos de build (bin/obj)
```

## Pacotes NuGet
```bash
dotnet add package NomeDoPacote          # adiciona um pacote
dotnet remove package NomeDoPacote       # remove um pacote
dotnet list package                      # lista pacotes instalados
```

## Gerenciar solution (.sln)
```bash
dotnet sln add Pasta/Projeto.csproj      # adiciona projeto à solution
dotnet sln remove Pasta/Projeto.csproj   # remove projeto da solution
dotnet sln list                          # lista projetos na solution
```

## Referências entre projetos
```bash
dotnet add ProjetoA reference ProjetoB   # ProjetoA passa a referenciar ProjetoB
```

## Testes
```bash
dotnet new xunit -o Testes    # cria projeto de testes com xUnit
dotnet test                   # roda os testes
```

## Info do ambiente
```bash
dotnet --version        # versão do SDK ativo
dotnet --list-sdks      # SDKs instalados
dotnet --list-runtimes  # runtimes instalados
```

## Fluxo típico para um projeto de console estruturado

```bash
cd ~/projects/Demos
dotnet new console -o Course
cd Course
# criar as pastas/arquivos Entities/Order.cs, Entities/Enums/OrderStatus.cs...
dotnet build
dotnet run
```

> Nota: rodar um `.cs` solto (ex: `dotnet run Program.cs`) usa o recurso de *file-based apps* do .NET 10 — o compilador considera só aquele arquivo, então outras classes/enums na mesma pasta não são enxergadas junto. Para múltiplos arquivos se compilarem juntos (IntelliSense incluso), é necessário um projeto real com `.csproj`.
