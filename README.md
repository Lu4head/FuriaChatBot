### Projeto criado para o Desafio Tecnico para vaga de Estagiário de Engenharia de Software na Furia
Autor: Luan Emanuel Rinaldi Argentato
Data: 26/04/2025

# ChatBot Furia com Inteligência Artifical para WhatsApp

Este README fornece informações essenciais sobre como configurar e executar o projeto em seu ambiente local, e sobre o funcionamento do projeto.

## Requisitos

Certifique-se de que você tenha os seguintes requisitos instalados em seu sistema:

- Python (versão recomendada: 3.12 ou superior)
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
docker-compose up --build api
```
```bash
docker-compose up --build waha
```

## Acessando a Aplicação

Por padrão, a aplicação WAHA estará disponível em http://localhost:3000.

Ao acessar a página de Dashboard você pode configurar seu número de celular ao qual o Bot irá responder.

Após configurado o número adicionar o webhook à configuraçao para fechar a comunicação com a API : "URL: http://api:5000/chatbot/webhook/"

## Funcionamento do Chatbot

A aplicação utiliza para conexão com o WhatsApp o container Waha que fornece uma integração e uma API para troca de dados entre o WhatsApp e seu serviço criado.

Após coletada sua mensagem recebida no número configurado essa é passada para uma Rota configurada numa API Flask que irá processar a mensagem identificando dados do destinatário e o conteúdo da mensagem, além do histórico de conversa com o destinatário.

Após o processamento da mensagem o conteúdo é enviado para um modelo de IA com o serviço da Groq AI que irá responder a mensagem com base no histórico de conversa e no conteúdo da mensagem.

A aplicação também possui um banco de dados vetorizado onde podem ser armazenados dados de contexto para o modelo de IA, como dados da Furia, sua história, ações e times para assim gerar uma resposta mais assertiva.     
