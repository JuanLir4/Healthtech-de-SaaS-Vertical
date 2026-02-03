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
    
class DespesaSimples(BaseModel):
    valor: float
       
class OperadoraDespesasRaz(BaseModel):
    razao_social: str
    despesas: List[DespesaSimples]
    
class OperadoraDespesasResponseUF(BaseModel):
    uf: str
    despesas: float