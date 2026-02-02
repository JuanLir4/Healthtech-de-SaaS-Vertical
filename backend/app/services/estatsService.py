import pandas as pd
from cachetools import TTLCache, cached

#aqui vou usar pandas (melhor pra chegar nas estatisticas)
#e vou usar a abondagem "Cachear resultado por X minutos", dessa forma nao precisa recalcular a cada requisição
#e fica solido com a relação a possivel mudança dos dados



cache = TTLCache(maxsize=1, ttl=600)  # 10 minutos

@cached(cache)
def calcularEstatisticas():
    df = pd.read_csv("C:/Users/Juan/Desktop/TesteTecnicoIntuitive/data/arquivosDescomp/despesas_agregadas.csv", sep=";")
    top5= df.sort_values('ValorDespesa', ascending=False).head(5)
    listaTop5 = top5['Razao_Social'].tolist()
   
    totalDespesas = df['ValorDespesa'].sum()
    mediaDespesas = df['ValorDespesa'].mean()
    
    
    return {
    
    "totalDespesas": totalDespesas,
    "mediaDespesas": mediaDespesas, 
    "operadoresTop5": listaTop5
    
    }
    