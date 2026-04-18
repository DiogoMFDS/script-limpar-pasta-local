# Template de Scripts Python

Este é um template básico para projetos de automação e scripts em Python. Ele fornece uma estrutura organizada para desenvolvimento rápido e manutenção fácil.

## Descrição

O template inclui:
- Estrutura modular com separação de configurações, modelos e módulos.
- Configurações de ambiente virtual.
- Logs integrados.
- Suporte a depuração no VS Code.

## Pré-requisitos

- Python 3.8 ou superior
- Git (opcional, para versionamento)

## Instalação

1. Clone ou baixe este repositório:
   ```bash
   git clone https://github.com/DiogoMFDS/templateScripts.git
   cd templateScripts
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
- Configure o depurador conforme `.vscode/launch.json`.
- Edite os arquivos em `App/` para personalizar a lógica.

### Estrutura do Projeto
```
templateScripts/
├── .vscode/           # Configurações do VS Code
├── App/               # Código principal
│   ├── __main__.py    # Ponto de entrada
│   ├── config/        # Configurações
│   ├── libs/          # Bibliotecas auxiliares
│   ├── Models/        # Modelos de dados
│   └── Modules/       # Módulos funcionais
├── logs/              # Arquivos de log
├── executar.bat       # Script de execução para Windows
├── requirements.txt   # Dependências Python
└── README.md          # Este arquivo
```

## Personalização

- **Configurações**: Edite `App/config/config_app.py` e os arquivos `.ini` em `config/init/`.
- **Lógica**: Adicione funções em `App/Modules/` e importe em `__main__.py`.
- **Dependências**: Adicione pacotes em `requirements.txt`.

## Depuração

Use o VS Code para depurar:
1. Abra o projeto.
2. Pressione F5 ou vá para Run > Start Debugging.
3. Selecione uma configuração (Arquivo Atual ou Módulo Principal).

## Logs

Os logs são salvos em `logs/`. Configure em `App/config/config_log.py`.


