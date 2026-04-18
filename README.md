# Script Limpar Pasta Local

Este é um script em Python para limpar pastas locais, removendo arquivos modificados há mais de 15 dias. Ele fornece uma estrutura organizada para automação e manutenção fácil de diretórios.

## Descrição

O script inclui:
- Estrutura modular com separação de configurações, bibliotecas auxiliares e módulos funcionais.
- Configurações de ambiente virtual.
- Logs integrados para rastreamento de operações.
- Suporte a depuração no VS Code (opcional).

## Funcionalidades

- Remove arquivos modificados antes de uma data limite (padrão: 15 dias atrás).
- Analisa recursivamente subpastas.
- Registra operações em logs para auditoria.
- Configurável via arquivos .ini.

## Pré-requisitos

- Python 3.8 ou superior
- Git (opcional, para versionamento)

## Instalação

1. Clone ou baixe este repositório:
   ```bash
   git clone https://github.com/DiogoMFDS/script-limpar-pasta-local.git
   cd script-limpar-pasta-local
   ```

2. Crie e ative o ambiente virtual:
   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

### Configuração
Edite o arquivo `App/Config/init/prod.ini` para definir o caminho da pasta a ser limpa:
```
[CAMINHOS]
caminho = C:\caminho\para\pasta
```

### Execução Direta
Execute o script principal:
```bash
python -m App
```
Ou use o arquivo batch:
```bash
executar.bat
```

### Desenvolvimento
- Abra no VS Code.
- Edite os arquivos em `App/` para personalizar a lógica.
- Configure o depurador se necessário.

### Estrutura do Projeto
```
script-limpar-pasta-local/
├── App/               # Código principal
│   ├── __main__.py    # Ponto de entrada
│   ├── Config/        # Configurações
│   │   ├── config_app.py
│   │   ├── config_log.py
│   │   ├── icon/
│   │   └── init/
│   │       ├── dev.ini
│   │       └── prod.ini
│   ├── Libs/          # Bibliotecas auxiliares
│   │   ├── __init__.py
│   │   └── apoio.py
│   └── Modules/       # Módulos funcionais
│       ├── __init__.py
│       └── funcao.py
├── logs/              # Arquivos de log
├── executar.bat       # Script de execução para Windows
├── requirements.txt   # Dependências Python
└── README.md          # Este arquivo
```

## Personalização

- **Configurações**: Edite `App/Config/config_app.py` e os arquivos `.ini` em `App/Config/init/`.
- **Lógica**: Adicione ou modifique funções em `App/Modules/` e importe em `__main__.py`.
- **Dependências**: Adicione pacotes em `requirements.txt`.

## Logs

Os logs são salvos em `logs/`. Configure em `App/Config/config_log.py`.


