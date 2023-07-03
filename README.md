# Microservice FastAPI

Este é um projeto de microserviço em FastAPI.

## Instalação


1. Crie e ative um ambiente virtual:

python -m venv venv
source venv/bin/activate # Linux/macOS
venv\Scripts\activate # Windows

2. Instale as dependências:

pip install -r requirements.txt

## Uso

1. Inicie o servidor:

uvicorn main:app --reload



2. Acesse a documentação da API em seu navegador:

http://localhost:8000/docs

de

3. Explore os endpoints disponíveis para interagir com os pacientes e medições.

## Testes

1. Certifique-se de ter ativado o ambiente virtual.

2. Execute os testes:

python -m unittest discover app

