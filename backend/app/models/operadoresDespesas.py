from pydantic import BaseModel
from typing import List

#vou criar so um modelo aqui, e apartir desse modelo extrair informações de diferentes tabelas

class Despesa(BaseModel):
    ano: int
    trimestre: int
    descricao: str
    valor: float
    
class OperadoraDespesasResponse(BaseModel):
    cnpj: str
    despesas: List[Despesa]
    
class OperadoraDespesasResponseUF(BaseModel):
    uf: str
    despesas: float