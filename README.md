# API Raízes do Nordeste 🌵

API REST desenvolvida em **Python + FastAPI** para gerenciamento de pedidos da rede de restaurantes **Raízes do Nordeste**.

O sistema permite cadastro de usuários, autenticação, gerenciamento de produtos, criação de pedidos, processamento de pagamento mock e controle de fidelidade.

---

# Tecnologias utilizadas

* Python
* FastAPI
* SQLAlchemy
* SQLite
* JWT (Autenticação)
* Swagger / OpenAPI
* Uvicorn

---

# Arquitetura do projeto

O projeto foi organizado em camadas para separar responsabilidades:

```
app
│
├── core
│   ├── auth.py
│   └── config.py
│
├── routes
│   ├── auth_routes.py
│   ├── fidelidade_routes.py
│   ├── pagamentos_routes.py
│   ├── pedidos_routes.py
│   └── produtos_routes.py
│
├── services
│   ├── auth_service.py
│   ├── pagamento_mock_service.py
│   └── pedido_service.py
│
├── database.py
├── main.py
├── models.py
└── schemas.py
```

### Camadas

**routes**

* Define os endpoints da API

**services**

* Contém regras de negócio

**core**

* Configurações e autenticação

**models**

* Estrutura do banco de dados

**schemas**

* Validação de dados com Pydantic

---

# Como executar o projeto

## 1 - Clonar repositório

```
git clone https://github.com/GabrielHPrado/PROJETO_RAIZES
```

---

## 2 - Entrar na pasta

```
cd PROJETO_RAIZES
```

---

## 3 - Criar ambiente virtual

```
python -m venv venv
```

---

## 4 - Ativar ambiente

### Windows

```
venv\Scripts\activate
```

### Linux / Mac

```
source venv/bin/activate
```

---

## 5 - Instalar dependências

```
pip install -r requirements.txt
```

---

## 6 - Rodar a API

```
uvicorn app.main:app --reload
```

---

# Documentação da API

Após iniciar o servidor, acesse:

Swagger:

```
http://localhost:8000/docs
```

ReDoc:

```
http://localhost:8000/redoc
```

---

# Endpoints principais

## Autenticação

```
POST /auth/register
POST /auth/login
```

---

## Produtos

```
GET /produtos
POST /produtos
```

---

## Pedidos

```
POST /pedidos
GET /pedidos
PATCH /pedidos/{id}/status
```

---

## Pagamentos

```
POST /pagamentos
```

Pagamento é simulado (**mock**).

---

## Fidelidade

```
GET /fidelidade
POST /fidelidade
```

Permite gerenciar pontos de clientes.

---

# Fluxo principal do sistema

1. Criar usuário
2. Realizar login
3. Cadastrar produtos
4. Criar pedido
5. Processar pagamento mock
6. Atualizar status do pedido
7. Acumular pontos de fidelidade

---

# Banco de dados

O projeto utiliza **SQLite** para armazenamento local.

O banco é criado automaticamente ao iniciar a aplicação:

```
database.db
```

---

# Testes da API

Os testes podem ser realizados através de:

* Swagger (`/docs`)
* Postman

Arquivo da coleção incluído no projeto:

```
postman_collection.json
```

---

# Autor

Desenvolvido por **Gabriel HENRIQUE PEREIRA Prado**
MATRICULA **4470123**

Projeto acadêmico para estudo de **Back-End com Python e FastAPI**.
