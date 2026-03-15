import random
from fastapi import APIRouter

router = APIRouter(
    prefix="/pagamentos",
    tags=["Pagamentos"]
)


@router.post("/")
def processar_pagamento():

    resultado = random.choice(["APROVADO", "NEGADO"])

    return {
        "status_pagamento": resultado
    }