### Projeto criado para o Desafio Tecnico para vaga de Estagiário de Engenharia de Software na Furia
Autor: Luan Emanuel Rinaldi Argentato
Data: 26/04/2025

# ChatBot Furia com Inteligência Artifical para WhatsApp

Este README fornece informações essenciais sobre como configurar e executar o projeto em seu ambiente local.

## Requisitos

Certifique-se de que você tenha os seguintes requisitos instalados em seu sistema:

- Python (versão recomendada: 3.10 ou superior)
- Docker e docker compose
- Outras dependências listadas no arquivo `requirements.txt`


## Instalação das Dependências

Criar ambiente virtual
```bash
python -m venv venv
```

Ativar ambiente virtual (Linux/MacOS)
```bash
source venv/bin/activate
```

Ativar ambiente virtual (Windows)
```bash
venv\Scripts\activate
```

Com o ambiente virtual ativado, instale as dependências do projeto usando o comando:
```bash
pip install -r requirements.txt
```


## Rodar o projeto

Após instalar as dependências, inicialize os serviços com docker-compose:
```bash
docker-compose up --build
```

## Acessando a Aplicação

Por padrão, a aplicação estará disponível em http://localhost:3000.
