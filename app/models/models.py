from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime, Enum
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import enum

Base = declarative_base()

class CanalPedido(enum.Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    BALCAO = "BALCAO"
    PICKUP = "PICKUP"
    WEB = "WEB"

class StatusPedido(enum.Enum):
    AGUARDANDO_PAGAMENTO = "AGUARDANDO_PAGAMENTO"
    PAGAMENTO_CONFIRMADO = "PAGAMENTO_CONFIRMADO"
    EM_PREPARO = "EM_PREPARO"
    PRONTO = "PRONTO"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    senha = Column(String)
    consentimento_lgpd = Column(Boolean, default=False)
    data_consentimento = Column(DateTime, nullable=True)
    
    # Relacionamentos
    pedidos = relationship("Pedido", back_populates="usuario")
    pontos_fidelidade = relationship("Fidelidade", back_populates="cliente")
    auditorias = relationship("Auditoria", back_populates="usuario")

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    descricao = Column(String)
    preco = Column(Float)
    
    # Relacionamentos
    estoque = relationship("Estoque", back_populates="produto", uselist=False)
    itens_pedido = relationship("ItemPedido", back_populates="produto")

class Estoque(Base):
    __tablename__ = "estoques"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    unidade_id = Column(Integer, default=1)
    quantidade = Column(Integer, default=0)
    
    # Relacionamentos
    produto = relationship("Produto", back_populates="estoque")

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    canal_pedido = Column(Enum(CanalPedido), nullable=False)
    status = Column(Enum(StatusPedido), default=StatusPedido.AGUARDANDO_PAGAMENTO)
    valor_total = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relacionamentos
    usuario = relationship("Usuario", back_populates="pedidos")
    itens = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")
    pagamento = relationship("Pagamento", back_populates="pedido", uselist=False)
    pontos_fidelidade = relationship("Fidelidade", back_populates="pedido")
    auditorias = relationship("Auditoria", back_populates="pedido")

class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    quantidade = Column(Integer)
    preco_unitario = Column(Float)

    # Relacionamentos
    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto", back_populates="itens_pedido")

class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), unique=True)
    valor = Column(Float)
    metodo = Column(String)
    status = Column(String)
    transacao_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relacionamentos
    pedido = relationship("Pedido", back_populates="pagamento")

class Fidelidade(Base):
    __tablename__ = "fidelidade"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"))
    pontos = Column(Integer, default=0)
    tipo = Column(String)  # ACUMULO, RESGATE
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relacionamentos
    cliente = relationship("Usuario", back_populates="pontos_fidelidade")
    pedido = relationship("Pedido", back_populates="pontos_fidelidade")

class Auditoria(Base):
    __tablename__ = "auditorias"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=True)
    acao = Column(String)
    dados_anteriores = Column(String, nullable=True)  # JSON string
    dados_novos = Column(String, nullable=True)       # JSON string
    created_at = Column(DateTime, default=datetime.now)
    
    # Relacionamentos
    usuario = relationship("Usuario", back_populates="auditorias")
    pedido = relationship("Pedido", back_populates="auditorias")