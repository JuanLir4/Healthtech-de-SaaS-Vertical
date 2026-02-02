from fastapi import APIRouter, HTTPException
from app.services.estatsService import calcularEstatisticas
from app.models.Estats import Estats

router = APIRouter(
    prefix="/api/estatisticas",
    tags=["Operadoras"]
)

@router.get("/", response_model=Estats)
def getEstats():
    
    return calcularEstatisticas()