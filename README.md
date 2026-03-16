# 🌵 API Raízes do Nordeste

API REST desenvolvida em **Python + FastAPI** para gerenciamento de pedidos da rede de restaurantes **Raízes do Nordeste**.

O sistema permite:

* cadastro de usuários
* autenticação com perfis de acesso
* gerenciamento de produtos
* criação de pedidos multicanal
* processamento de pagamento mock
* programa de fidelidade
* conformidade com LGPD

---

# 📋 Funcionalidades

* 🔐 **Autenticação JWT** com perfis de acesso
* 👤 **Cadastro de usuários** com consentimento LGPD
* 🍽 **Gestão de produtos** com controle de estoque
* 🧾 **Criação de pedidos** com multicanalidade
* 💳 **Pagamento mock** simulando gateway externo
* ⭐ **Programa de fidelidade** (1 ponto a cada R$10)
* 📦 **Validação de estoque** antes do pedido
* 📊 **Auditoria de ações sensíveis**
* ⚖ **Conformidade com LGPD**
* 📄 **Paginação em listagens**
* 🔎 **Filtros por canal de pedido**
* ❗ **Tratamento padronizado de erros**
* 📚 **Documentação automática Swagger / OpenAPI**

---

# 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Função              |
| ---------- | ------ | ------------------- |
| Python     | 3.9+   | Linguagem principal |
| FastAPI    | 0.104+ | Framework Web       |
| SQLAlchemy | 2.0+   | ORM                 |
| SQLite     | 3.x    | Banco de dados      |
| JWT        | -      | Autenticação        |
| bcrypt     | 4.0+   | Hash de senha       |
| Pydantic   | 2.0+   | Validação de dados  |
| Uvicorn    | 0.24+  | Servidor ASGI       |

---

# 🏗️ Arquitetura do Projeto

O projeto foi organizado em **camadas**, separando responsabilidades.

```
app/

core/
├── auth_deps.py
├── config.py
├── database.py
└── security.py

models/
└── models.py

routes/
├── auth_routes.py
├── produtos_routes.py
├── pedidos_routes.py
├── pagamentos_routes.py
└── fidelidade_routes.py

schemas/
└── schemas.py

services/
├── auth_service.py
├── pedido_service.py
└── pagamento_mock_service.py

database.py
main.py
seed.py
```

---

# 📚 Camadas da Aplicação

| Camada   | Responsabilidade          |
| -------- | ------------------------- |
| routes   | Endpoints da API          |
| services | Regras de negócio         |
| models   | Entidades do banco        |
| schemas  | Validação com Pydantic    |
| core     | Segurança e configurações |

---

# 🔐 Perfis de Acesso

O sistema possui **4 níveis de permissão**:

| Perfil    | Permissões                    |
| --------- | ----------------------------- |
| ADMIN     | Acesso total ao sistema       |
| GERENTE   | Gerenciar produtos            |
| ATENDENTE | Criar pedidos                 |
| CLIENTE   | Acessar seus próprios pedidos |

---

# 🚀 Como Executar o Projeto

## 1️⃣ Clonar o repositório

```bash
git clone https://github.com/GabrielHPrado/PROJETO_RAIZES
```

## 2️⃣ Entrar na pasta

```bash
cd PROJETO_RAIZES
```

## 3️⃣ Criar ambiente virtual

```bash
python -m venv venv
```

## 4️⃣ Ativar ambiente virtual

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

## 5️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

## 6️⃣ Criar usuário ADMIN (opcional)

```bash
python seed.py
```

Usuário criado:

| Campo | Valor                                       |
| ----- | ------------------------------------------- |
| Email | [admin@raizes.com](mailto:admin@raizes.com) |
| Senha | admin123                                    |

## 7️⃣ Executar a API

```bash
uvicorn app.main:app --reload
```

A API estará disponível em:

```
http://localhost:8000
```

---

# 📚 Documentação da API

| Documentação | URL                                                                      |
| ------------ | ------------------------------------------------------------------------ |
| Swagger UI   | [http://localhost:8000/docs](http://localhost:8000/docs)                 |
| ReDoc        | [http://localhost:8000/redoc](http://localhost:8000/redoc)               |
| OpenAPI JSON | [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json) |

---

# 🔌 Endpoints Principais

## 🔐 Autenticação

| Método | Endpoint        | Descrição         |
| ------ | --------------- | ----------------- |
| POST   | /auth/registrar | Registrar usuário |
| POST   | /auth/login     | Login (JWT)       |
| POST   | /auth/token     | Login OAuth2      |

---

## 🍽 Produtos

| Método | Endpoint                   | Acesso          |
| ------ | -------------------------- | --------------- |
| GET    | /produtos/?page=1&limit=10 | Autenticado     |
| GET    | /produtos/todos            | Autenticado     |
| GET    | /produtos/{id}             | Autenticado     |
| POST   | /produtos/                 | ADMIN / GERENTE |
| PUT    | /produtos/{id}             | ADMIN / GERENTE |
| DELETE | /produtos/{id}             | ADMIN           |

---

## 🧾 Pedidos

| Método | Endpoint                         | Acesso      |
| ------ | -------------------------------- | ----------- |
| POST   | /pedidos/                        | Autenticado |
| GET    | /pedidos/?canalPedido=APP&page=1 | Autenticado |
| GET    | /pedidos/{id}                    | Autenticado |

---

## 💳 Pagamentos

| Método | Endpoint                          |
| ------ | --------------------------------- |
| POST   | /pagamentos/processar/{pedido_id} |

---

## ⭐ Fidelidade

| Método | Endpoint                        |
| ------ | ------------------------------- |
| GET    | /fidelidade/pontos/{cliente_id} |

---

# 💳 Pagamento Mock

O pagamento simulado utiliza as seguintes probabilidades:

| Resultado | Probabilidade |
| --------- | ------------- |
| Aprovado  | 70%           |
| Recusado  | 20%           |
| Erro      | 10%           |

### Exemplo de resposta

```json
{
  "pedido_id": 1,
  "status": "APROVADO",
  "transacao_id": "MOCK_ABC123",
  "mensagem": "Transação aprovada",
  "processado_em": "2026-03-16T10:31:00"
}
```

---

# 🔄 Fluxo do Sistema

```
Criar Usuário
      ↓
Fazer Login
      ↓
Cadastrar Produtos
      ↓
Criar Pedido
      ↓
Validar Estoque
      ↓
Processar Pagamento
      ↓
Atualizar Status
      ↓
Acumular Pontos
```

---

# 🗄️ Banco de Dados

O sistema utiliza **SQLite**.

Arquivo gerado automaticamente:

```
database.db
```

### Tabelas principais

| Tabela       | Descrição           |
| ------------ | ------------------- |
| usuarios     | Usuários do sistema |
| produtos     | Produtos            |
| estoques     | Controle de estoque |
| pedidos      | Pedidos             |
| itens_pedido | Itens dos pedidos   |
| pagamentos   | Pagamentos          |
| fidelidade   | Pontos              |
| auditorias   | Log de ações        |

---

# 🧪 Testes da API

A API pode ser testada com:

* Swagger UI
* Postman
* Insomnia

Arquivo incluído:

```
postman_collection.json
```

### Cenários de teste

| ID  | Descrição                   | Tipo     |
| --- | --------------------------- | -------- |
| T01 | Registrar usuário com LGPD  | Positivo |
| T02 | Registrar sem LGPD          | Negativo |
| T03 | Login válido                | Positivo |
| T04 | Login inválido              | Negativo |
| T05 | Criar produto (admin)       | Positivo |
| T06 | Criar produto sem permissão | Negativo |
| T07 | Criar pedido com estoque    | Positivo |
| T08 | Criar pedido sem estoque    | Negativo |
| T09 | Pagamento aprovado          | Positivo |
| T10 | Pagamento recusado          | Positivo |
| T11 | Consultar pontos            | Positivo |
| T12 | Buscar pedido inexistente   | Negativo |

---

# 📄 Licença

MIT License
© 2026 Gabriel Henrique Pereira Prado

---

# 👨‍💻 Autor

**Gabriel Henrique Pereira Prado**

🎓 Matrícula: 4470123

GitHub:
[https://github.com/GabrielHPrado](https://github.com/GabrielHPrado)


