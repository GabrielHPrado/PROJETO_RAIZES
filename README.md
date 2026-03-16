# API Raízes do Nordeste 🌵

API REST desenvolvida em **Python + FastAPI** para gerenciamento de pedidos da rede de restaurantes **Raízes do Nordeste**.

O sistema permite cadastro de usuários, autenticação com perfis de acesso, gerenciamento de produtos, criação de pedidos com multicanalidade, processamento de pagamento mock, controle de fidelidade e conformidade com LGPD.

---

## 📋 Funcionalidades

- ✅ **Autenticação JWT** com perfis de acesso (ADMIN, GERENTE, ATENDENTE, CLIENTE)
- ✅ **Cadastro de usuários** com consentimento LGPD
- ✅ **Gestão de produtos** com controle de estoque
- ✅ **Criação de pedidos** com multicanalidade (APP, TOTEM, BALCÃO, PICKUP, WEB)
- ✅ **Pagamento mock** simulando gateway externo (70% aprovação, 20% recusa, 10% erro)
- ✅ **Programa de fidelidade** (1 ponto a cada R$10 em compras)
- ✅ **Validação de estoque** antes da confirmação do pedido
- ✅ **Auditoria** de ações sensíveis
- ✅ **Conformidade com LGPD** (consentimento explícito, minimização de dados)
- ✅ **Paginação** em listagens
- ✅ **Filtros** por canal de pedido
- ✅ **Tratamento padronizado de erros**
- ✅ **Documentação interativa** com Swagger/OpenAPI

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Versão | Finalidade |
|:---|:---|:---|
| Python | 3.9+ | Linguagem principal |
| FastAPI | 0.104+ | Framework web |
| SQLAlchemy | 2.0+ | ORM (Mapeamento Objeto-Relacional) |
| SQLite | 3.x | Banco de dados |
| JWT | - | Autenticação stateless |
| bcrypt | 4.0+ | Hash de senhas |
| Pydantic | 2.0+ | Validação de dados |
| Uvicorn | 0.24+ | Servidor ASGI |

---

## 🏗️ Arquitetura do projeto

O projeto foi organizado em camadas para separar responsabilidades:
app
│
├── core/ # Configurações e segurança
│ ├── auth_deps.py # Dependências de autenticação
│ ├── config.py # Configurações do projeto
│ ├── database.py # Conexão com banco de dados
│ └── security.py # Funções de hash e JWT
│
├── models/
│ └── models.py # Modelos do banco de dados (SQLAlchemy)
│
├── routes/ # Endpoints da API
│ ├── auth_routes.py # Autenticação (registro/login)
│ ├── produtos_routes.py # CRUD de produtos
│ ├── pedidos_routes.py # Gestão de pedidos
│ ├── pagamentos_routes.py # Processamento de pagamentos
│ └── fidelidade_routes.py # Consulta de pontos
│
├── schemas/
│ └── schemas.py # Schemas Pydantic (validação)
│
├── services/ # Regras de negócio
│ ├── auth_service.py # Lógica de autenticação
│ ├── pedido_service.py # Lógica de pedidos
│ └── pagamento_mock_service.py # Simulação de pagamento
│
├── database.py # Sessão do banco de dados
├── main.py # Ponto de entrada da aplicação
└── seed.py # Script para criar usuário admin

text

### Camadas e responsabilidades

| Camada | Responsabilidade |
|:---|:---|
| **routes** | Endpoints, validação de entrada, respostas HTTP |
| **services** | Regras de negócio, orquestração de processos |
| **models** | Entidades e relacionamentos do banco de dados |
| **schemas** | Validação de dados com Pydantic |
| **core** | Configurações, segurança e utilidades |

---

## 🔐 Perfis de acesso

O sistema possui 4 perfis com diferentes níveis de permissão:

| Perfil | Permissões |
|:---|:---|
| **ADMIN** | Acesso total ao sistema |
| **GERENTE** | Gerenciar produtos e visualizar relatórios |
| **ATENDENTE** | Criar pedidos no balcão |
| **CLIENTE** | Apenas seus próprios pedidos |

---

## 🚀 Como executar o projeto

### Pré-requisitos

- Python 3.9 ou superior
- Git

### Passo a passo

#### 1 - Clonar repositório

```bash
git clone https://github.com/GabrielHPrado/PROJETO_RAIZES
2 - Entrar na pasta
bash
cd PROJETO_RAIZES
3 - Criar ambiente virtual
bash
python -m venv venv
4 - Ativar ambiente virtual
Windows:

bash
venv\Scripts\activate
Linux / Mac:

bash
source venv/bin/activate
5 - Instalar dependências
bash
pip install -r requirements.txt
6 - Criar usuário ADMIN (opcional)
bash
python seed.py
Isso criará o usuário:

Email: admin@raizes.com

Senha: admin123

7 - Rodar a API
bash
uvicorn app.main:app --reload
A API estará disponível em: http://localhost:8000

📚 Documentação da API
Após iniciar o servidor, acesse:

Documentação	URL
Swagger UI	http://localhost:8000/docs
ReDoc	http://localhost:8000/redoc
OpenAPI JSON	http://localhost:8000/openapi.json
🔌 Endpoints principais
Autenticação
Método	Endpoint	Descrição	Acesso
POST	/auth/registrar	Registrar novo usuário	Público
POST	/auth/login	Login (retorna JWT)	Público
POST	/auth/token	Login para OAuth2 (Swagger)	Público
Produtos
Método	Endpoint	Descrição	Acesso
GET	/produtos/?page=1&limit=10	Listar produtos (paginado)	Autenticado
GET	/produtos/todos	Listar todos produtos	Autenticado
GET	/produtos/{id}	Buscar produto por ID	Autenticado
POST	/produtos/	Criar produto	ADMIN/GERENTE
PUT	/produtos/{id}	Atualizar produto	ADMIN/GERENTE
DELETE	/produtos/{id}	Deletar produto	ADMIN
Pedidos
Método	Endpoint	Descrição	Acesso
POST	/pedidos/	Criar pedido	Autenticado
GET	/pedidos/?canalPedido=APP&page=1	Listar pedidos com filtros	Autenticado
GET	/pedidos/{id}	Buscar pedido por ID	Autenticado
Pagamentos
Método	Endpoint	Descrição	Acesso
POST	/pagamentos/processar/{pedido_id}	Processar pagamento mock	Autenticado
Fidelidade
Método	Endpoint	Descrição	Acesso
GET	/fidelidade/pontos/{cliente_id}	Consultar pontos	Autenticado
💳 Pagamento Mock
O pagamento é simulado com as seguintes probabilidades:

✅ 70% - Aprovado

❌ 20% - Recusado

⚠️ 10% - Erro

Exemplo de resposta (aprovado):

json
{
  "pedido_id": 1,
  "status": "APROVADO",
  "transacao_id": "MOCK_ABC123",
  "mensagem": "Transação aprovada",
  "processado_em": "2026-03-16T10:31:00"
}
🔄 Fluxo principal do sistema
text
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  1.     │    │  2.     │    │  3.     │    │  4.     │
│ Criar   │───▶│ Fazer   │───▶│ Cadastrar│───▶│ Criar   │
│ Usuário │    │ Login   │    │ Produtos │    │ Pedido  │
└─────────┘    └─────────┘    └─────────┘    └────┬────┘
                                                    │
                                                    ▼
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  7.     │    │  6.     │    │  5.     │    │  4.     │
│Acumular │◀───│ Atualizar│◀───│Processar│◀───│ Validar │
│ Pontos  │    │  Status │    │Pagamento│    │ Estoque │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
🗄️ Banco de dados
O projeto utiliza SQLite para armazenamento local.

Principais tabelas
Tabela	Descrição
usuarios	Usuários do sistema (com perfis)
produtos	Produtos do cardápio
estoques	Controle de estoque por produto
pedidos	Pedidos realizados
itens_pedido	Itens de cada pedido
pagamentos	Registro de pagamentos
fidelidade	Pontos de fidelidade
auditorias	Log de ações sensíveis
O banco é criado automaticamente ao iniciar a aplicação:

text
database.db
🧪 Testes da API
Os testes podem ser realizados através de:

Swagger UI (/docs) - Testes interativos

Postman/Insomnia - Coleção incluída

Arquivo da coleção incluído no projeto:

text
postman_collection.json
Cenários de teste (12 cenários)
ID	Descrição	Tipo
T01	Registrar usuário com LGPD	Positivo
T02	Registrar sem consentimento LGPD	Negativo
T03	Login com credenciais válidas	Positivo
T04	Login com senha incorreta	Negativo
T05	Criar produto (admin)	Positivo
T06	Criar produto sem permissão	Negativo
T07	Criar pedido com estoque	Positivo
T08	Criar pedido sem estoque	Negativo
T09	Pagamento aprovado	Positivo
T10	Pagamento recusado	Positivo
T11	Consultar pontos	Positivo
T12	Buscar pedido inexistente	Negativo
📄 Licença
MIT License © 2026 Gabriel Henrique Pereira Prado

👨‍💻 Autor
Gabriel Henrique Pereira Prado

Matrícula: 4470123

GitHub: @GabrielHPrado

E-mail: gabrielhprado0@gmail.com

