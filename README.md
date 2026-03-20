🌵 API Raízes do Nordeste

API REST desenvolvida em Python com FastAPI para gerenciamento de pedidos da rede de restaurantes Raízes do Nordeste.

O sistema permite:

- Cadastro de usuários
- Autenticação com perfis de acesso
- Gerenciamento de produtos
- Criação de pedidos multicanal
- Processamento de pagamento mock
- Programa de fidelidade
- Conformidade com LGPD

---

## 📋 Funcionalidades

- 🔐 Autenticação JWT com perfis de acesso
- 👤 Cadastro de usuários com consentimento LGPD
- 🍽 Gestão de produtos com controle de estoque
- 🧾 Criação de pedidos com multicanalidade
- 💳 Pagamento mock simulando gateway externo
- ⭐ Programa de fidelidade (1 ponto a cada R$10)
- 📦 Validação de estoque antes do pedido
- 📊 Auditoria de ações sensíveis
- ⚖ Conformidade com LGPD
- 📄 Paginação em listagens
- 🔎 Filtros por canal de pedido
- ❗ Tratamento padronizado de erros
- 📚 Documentação automática Swagger / OpenAPI

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Função |
|-----------|--------|--------|
| Python | 3.9+ | Linguagem principal |
| FastAPI | 0.104+ | Framework Web |
| SQLAlchemy | 2.0+ | ORM |
| SQLite | 3.x | Banco de dados |
| JWT | - | Autenticação |
| bcrypt | 4.0+ | Hash de senha |
| Pydantic | 2.0+ | Validação |
| Uvicorn | 0.24+ | Servidor |

---

## 🏗️ Arquitetura do Projeto

Estrutura baseada em arquitetura em camadas:


app/
├── core/
├── models/
├── routes/
├── schemas/
├── services/
├── main.py
└── database.py


### 📚 Camadas

| Camada | Responsabilidade |
|--------|----------------|
| routes | Endpoints da API |
| services | Regras de negócio |
| models | Entidades do banco |
| schemas | Validação de dados |
| core | Segurança e configurações |

---

## 🔐 Perfis de Acesso

| Perfil | Permissões |
|--------|-----------|
| ADMIN | Acesso total |
| GERENTE | Gerenciar produtos |
| ATENDENTE | Criar pedidos |
| CLIENTE | Acessar pedidos próprios |

---

## 🚀 Como Executar o Projeto

### 1️⃣ Clonar repositório

git clone https://github.com/GabrielHPrado/PROJETO_RAIZES

cd PROJETO_RAIZES


### 2️⃣ Criar ambiente virtual

python -m venv venv


### 3️⃣ Ativar ambiente

Windows:

venv\Scripts\activate


Linux/Mac:

source venv/bin/activate


### 4️⃣ Instalar dependências

pip install -r requirements.txt


### 5️⃣ Configurar variáveis de ambiente

Crie um arquivo `.env` baseado no `.env.example`

### 6️⃣ Criar usuário ADMIN (opcional)

python seed.py


Usuário padrão:
- Email: admin@raizes.com
- Senha: admin123

### 7️⃣ Executar API

uvicorn app.main:app --reload


API disponível em:

http://localhost:8000


---

## 📚 Documentação da API

A documentação é gerada automaticamente via Swagger:

- Swagger UI: http://localhost:8000/docs  
- ReDoc: http://localhost:8000/redoc  
- OpenAPI JSON: http://localhost:8000/openapi.json  

---

## 🔌 Endpoints Principais

### 🔐 Autenticação
| Método | Endpoint |
|--------|---------|
| POST | /auth/registrar |
| POST | /auth/login |
| POST | /auth/token |

### 🍽 Produtos
| Método | Endpoint | Acesso |
|--------|----------|--------|
| GET | /produtos/ | Autenticado |
| POST | /produtos/ | ADMIN / GERENTE |

### 🧾 Pedidos
| Método | Endpoint |
|--------|----------|
| POST | /pedidos/ |
| GET | /pedidos/ |
| GET | /pedidos/{id} |

### 💳 Pagamentos
| Método | Endpoint |
|--------|----------|
| POST | /pagamentos/processar/{id} |

---

## 💳 Pagamento Mock

| Resultado | Probabilidade |
|----------|--------------|
| Aprovado | 70% |
| Recusado | 20% |
| Erro | 10% |

---

## 🔄 Fluxo do Sistema

Usuário → Login → Criar Pedido → Validar Estoque → Pagamento → Atualização → Fidelidade

---

## 🗄️ Banco de Dados

Banco utilizado: SQLite

Arquivo gerado:

database.db


---

## 🧪 Testes da API

Os testes podem ser realizados via:

- Swagger
- Postman
- Insomnia

### ▶️ Coleção Postman

https://documenter.getpostman.com/view/49270615/2sBXijHX4G

### ▶️ Como executar

1. Importar coleção no Postman  
2. Executar fluxo completo  
3. Validar respostas e erros  

---

## 📌 Observação

Todos os endpoints e regras de negócio estão documentados também no PDF acadêmico entregue.

---

## 📄 Licença

MIT License © 2026 Gabriel Henrique Pereira Prado

---

## 👨‍💻 Autor

Gabriel Henrique Pereira Prado  
RU: 4470123  

GitHub: https://github.com/GabrielHPrado