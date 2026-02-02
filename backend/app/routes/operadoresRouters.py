from fastapi import APIRouter, HTTPException, Query
from app.services.operadorasService import buscarCNPJ, listarOperadoras, buscarDespesas, buscarDespesasUF
from app.models.operadores import Operadora, ListaOperadora
from app.models.operadoresDespesas import OperadoraDespesasResponse, OperadoraDespesasResponseUF


router = APIRouter(
    prefix="/api/operadoras",
    tags=["Operadoras"]
)
#rota com paginação: Keyset Pagination
@router.get("/", response_model=ListaOperadora)
def get_operadoras(
    #query: função define q o parametro venha da url
    cursor: int | None = Query(None, description="Último registro recebido"),
    limit: int = Query(5, ge=1, le=100, description="Quantidade de itens por página")
):
    return listarOperadoras(cursor=cursor, limit=limit)
    

#rota de retornar infos:
@router.get("/{cnpj}", response_model=Operadora)
def get_operadora(cnpj: str):
    operadora = buscarCNPJ(cnpj)

    if not operadora:
        raise HTTPException(
            status_code=404,
            detail="Operadora não encontrada"
        )

    return operadora

#rota de retornar despesas:
@router.get("/cnpj/{cnpj}/despesas", response_model=OperadoraDespesasResponse)
def getOperadoraDespesa(cnpj: str):
    despesas = buscarDespesas(cnpj)
    
        
    if not despesas:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma despesa encontrada para este CNPJ"
        )
    
    return {
            "cnpj": cnpj,
            "despesas": despesas
            }
    
@router.get("/uf/{UF}/despesas", response_model=OperadoraDespesasResponseUF)
def getOperadoraDespesaUF(UF: str):
    despesas = buscarDespesasUF(UF)
    
        
    if not despesas:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma despesa encontrada para esta UF"
        )
    
    return {
            "uf": UF,
            "despesas": despesas
            }
 
       
        

