# API Raízes do Nordeste

Projeto de API REST desenvolvido em Python utilizando FastAPI para gerenciamento de pedidos da rede de restaurantes **Raízes do Nordeste**.

## Tecnologias

* Python
* FastAPI
* SQLAlchemy
* SQLite
* JWT (autenticação)
* Swagger

## Como executar o projeto

### 1 - Clonar repositório

```
git clone https://github.com/usuario/raizes-nordeste-api
```

### 2 - Entrar na pasta

```
cd raizes-nordeste-api
```

### 3 - Criar ambiente virtual

```
python -m venv venv
```

### 4 - Ativar ambiente

Windows:

```
venv\Scripts\activate
```

Linux/Mac:

```
source venv/bin/activate
```

### 5 - Instalar dependências

```
pip install -r requirements.txt
```

### 6 - Rodar API

```
uvicorn app.main:app --reload
```

## Acessar documentação

Swagger:

```
http://localhost:8000/docs
```

## Endpoints principais

### Autenticação

POST /auth/register
POST /auth/login

### Produtos

GET /produtos
POST /produtos

### Pedidos

POST /pedidos
GET /pedidos

## Estrutura do projeto

```
app/
  main.py
  models.py
  database.py
  schemas.py

routes/
  auth_routes.py
  produtos_routes.py
  pedidos_routes.py

services/
  pedido_service.py
```

## Fluxo principal

1. Criar usuário
2. Fazer login
3. Cadastrar produtos
4. Criar pedido
5. Processar pagamento (mock)
