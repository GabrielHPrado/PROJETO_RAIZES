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

class PerfilUsuario(enum.Enum): 
    ADMIN = "ADMIN"
    GERENTE = "GERENTE"
    ATENDENTE = "ATENDENTE"
    CLIENTE = "CLIENTE"

class TipoFidelidade(enum.Enum):
    ACUMULO = "ACUMULO"
    RESGATE = "RESGATE"
    BONUS = "BONUS"


class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)  
    email = Column(String(100), unique=True, index=True, nullable=False)
    senha = Column(String(255), nullable=False)  
    perfil = Column(Enum(PerfilUsuario), default=PerfilUsuario.CLIENTE, nullable=False)  
    consentimento_lgpd = Column(Boolean, default=False, nullable=False)
    data_consentimento = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now)  
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)  
    

    pedidos = relationship("Pedido", back_populates="usuario", cascade="all, delete-orphan")
    pontos_fidelidade = relationship("Fidelidade", back_populates="cliente", cascade="all, delete-orphan")
    auditorias = relationship("Auditoria", back_populates="usuario", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Usuario {self.email} - {self.perfil.value}>"

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, unique=True)  
    descricao = Column(String(500), nullable=True) 
    preco = Column(Float, nullable=False)
    ativo = Column(Boolean, default=True) 
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    estoque = relationship("Estoque", back_populates="produto", uselist=False, cascade="all, delete-orphan")
    itens_pedido = relationship("ItemPedido", back_populates="produto")
    
    def __repr__(self):
        return f"<Produto {self.nome} - R${self.preco}>"

class Estoque(Base):
    __tablename__ = "estoques"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id", ondelete="CASCADE"), unique=True, nullable=False)
    unidade_id = Column(Integer, default=1, nullable=False)
    quantidade = Column(Integer, default=0, nullable=False)
    quantidade_minima = Column(Integer, default=5)  
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    
    produto = relationship("Produto", back_populates="estoque")
    
    def __repr__(self):
        return f"<Estoque Produto {self.produto_id}: {self.quantidade} unidades>"
    
    def verificar_disponibilidade(self, quantidade_solicitada):
        return self.quantidade >= quantidade_solicitada
    
    def baixar_estoque(self, quantidade):
        if self.verificar_disponibilidade(quantidade):
            self.quantidade -= quantidade
            return True
        return False

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="RESTRICT"), nullable=False)
    canal_pedido = Column(Enum(CanalPedido), nullable=False)
    status = Column(Enum(StatusPedido), default=StatusPedido.AGUARDANDO_PAGAMENTO, nullable=False)
    valor_total = Column(Float, default=0, nullable=False)
    observacoes = Column(String(500), nullable=True)  
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
  
    usuario = relationship("Usuario", back_populates="pedidos")
    itens = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")
    pagamento = relationship("Pagamento", back_populates="pedido", uselist=False, cascade="all, delete-orphan")
    pontos_fidelidade = relationship("Fidelidade", back_populates="pedido")
    auditorias = relationship("Auditoria", back_populates="pedido")
    
    def __repr__(self):
        return f"<Pedido {self.id} - {self.status.value} - R${self.valor_total}>"
    
    def calcular_total(self):
        return sum(item.subtotal for item in self.itens)

class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id", ondelete="CASCADE"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id", ondelete="RESTRICT"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)  
    

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario


    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto", back_populates="itens_pedido")
    
    def __repr__(self):
        return f"<Item {self.produto_id} x{self.quantidade} - R${self.subtotal}>"

class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id", ondelete="CASCADE"), unique=True, nullable=False)
    valor = Column(Float, nullable=False)
    metodo = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False)  
    transacao_id = Column(String(100), unique=True, nullable=True)
    resposta_gateway = Column(String(500), nullable=True) 
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    
  
    pedido = relationship("Pedido", back_populates="pagamento")
    
    def __repr__(self):
        return f"<Pagamento {self.transacao_id} - {self.status}>"

class Fidelidade(Base):
    __tablename__ = "fidelidade"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    pontos = Column(Integer, default=0, nullable=False)
    tipo = Column(Enum(TipoFidelidade), nullable=False)  
    pedido_id = Column(Integer, ForeignKey("pedidos.id", ondelete="SET NULL"), nullable=True)
    descricao = Column(String(200), nullable=True) 
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    
  
    cliente = relationship("Usuario", back_populates="pontos_fidelidade")
    pedido = relationship("Pedido", back_populates="pontos_fidelidade")
    
    def __repr__(self):
        return f"<Fidelidade {self.cliente_id}: {self.pontos} pontos - {self.tipo.value}>"

class Auditoria(Base):
    __tablename__ = "auditorias"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id", ondelete="SET NULL"), nullable=True)
    acao = Column(String(100), nullable=False)
    entidade = Column(String(50), nullable=True)  
    entidade_id = Column(Integer, nullable=True)  
    dados_anteriores = Column(String(1000), nullable=True)  
    dados_novos = Column(String(1000), nullable=True)
    ip_address = Column(String(50), nullable=True) 
    user_agent = Column(String(200), nullable=True)  
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    
   
    usuario = relationship("Usuario", back_populates="auditorias")
    pedido = relationship("Pedido", back_populates="auditorias")
    
    def __repr__(self):
        return f"<Auditoria {self.acao} - {self.created_at}>"