from pydantic import BaseModel
from typing import List

#vou criar so um modelo aqui, e apartir desse modelo extrair informações de diferentes tabelas
class Estats(BaseModel):
    totalDespesas: float
    mediaDespesas: float
    operadoresTop5: List[str]
    