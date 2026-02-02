from fastapi import FastAPI
from app.routes.operadoresRouters import router as operadoras_router
from app.routes.estatisticasRoute import router as estatistica_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API de Operadoras")

app.include_router(operadoras_router)
app.include_router(estatistica_router)

# Configuração CORS
origins = [
    "http://localhost:5173",  
    "http://127.0.0.1:5173",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       
    allow_credentials=True,
    allow_methods=["*"],         
    allow_headers=["*"],          
)