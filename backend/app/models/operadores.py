from pydantic import BaseModel
from typing import List, Optional


#vou criar so um modelo aqui, e apartir desse modelo extrair informações de diferentes tabelas
class Operadora(BaseModel):
    cnpj: str
    razao_social: str
    nome_fantasia: str
    modalidade: str
    uf: str
    
class ListaOperadora(BaseModel):
    items: List[str]
    next_cursor: Optional[int]