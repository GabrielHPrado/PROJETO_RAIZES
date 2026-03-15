from pydantic import BaseModel


class UsuarioCreate(BaseModel):

    email: str
    senha: str


class ProdutoCreate(BaseModel):

    nome: str
    preco: float


class PedidoItem(BaseModel):

    produto_id: int
    quantidade: int


class PedidoCreate(BaseModel):

    cliente_id: int
    itens: list[PedidoItem]