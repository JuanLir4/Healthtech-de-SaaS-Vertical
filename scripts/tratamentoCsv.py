import pandas as pd
import os

#a ideia aqui é transformar qualquer arquivo em csv e 
# manter apenas as linhas que possuem Despesas com Eventos / Sinistros depois juntar os csv e tratar os dados
#OBS: O DATASET N POSSUI CNPJ E MTS COISAS, VAMOS TER Q LIGAR COM OUTRA BASE PUBLICA ATRAVES DO REG_ANS

#ENTAO PRIMEIRO PODEMOS SO CRIAR UM CSV UNICO COM DESPESAS E ETC, QUE POSSUI DATA E VALOR

#função para juntar os 3 trimestre em um unico csv e tratar com base em "Despesas com Eventos / Sinistros"

def consolidCsv(caminhos, caminhoPasta):
    # listaArquivos = os.listdir(caminho)
    
    dfFiltrados = []
    for caminhoTotal in caminhos:
        
       
        #lendo o dataframe
        df = pd.read_csv(caminhoTotal, sep=";")
        
        dfFiltrado= df[df["DESCRICAO"].str.contains("Despesas com Eventos / Sinistros", na=False)]
       
        #adcionando valor da despesa e removendo saldoinicial e saldo final
        dfFiltrado["VL_SALDO_INICIAL"] = df["VL_SALDO_INICIAL"].str.replace(",", ".", regex=False).astype(float)
        dfFiltrado["VL_SALDO_FINAL"] = df["VL_SALDO_FINAL"].str.replace(",", ".", regex=False).astype(float)
        dfFiltrado["ValorDespesa"] = dfFiltrado["VL_SALDO_FINAL"].astype(float) - dfFiltrado["VL_SALDO_INICIAL"].astype(float)
        dfFiltrado.drop('VL_SALDO_FINAL', axis=1, inplace=True)
        dfFiltrado.drop('VL_SALDO_INICIAL', axis=1, inplace=True)
        
        #colocando ano e trimestre:
        dfFiltrado['DATA'] = pd.to_datetime(dfFiltrado['DATA'])
        dfFiltrado.insert(0, 'ANO', dfFiltrado['DATA'].dt.year)
        dfFiltrado = dfFiltrado.drop(columns='DATA')
        
        trimestre = caminhoTotal[-10]
        dfFiltrado.insert(1, 'TRISMESTRE', trimestre)
        
        
        #salvando os df filtrados
        dfFiltrados.append(dfFiltrado)
    
    dfFinal = pd.concat(dfFiltrados, ignore_index=True)
    dfFinal.to_csv(f"{caminhoPasta}/resultado_final.csv", sep=";", index=False)
    
    
    #depois colocar o join aqui:
        
    return dfFinal

#vou usar essa função para juntar os csv's baseado no "REG_ANS" presente nas duas tabelas e
#fazer tratamento de dados
def joinCsv(df1, caminhoDf2):
   
    df2 = pd.read_csv(caminhoDf2, sep=";")
    
    #reduzindo a as colunas que vou usar
    df2 = df2[["REGISTRO_OPERADORA", "Razao_Social", "CNPJ", "Modalidade", "UF"]]
    df2.rename(columns={'REGISTRO_OPERADORA': 'REG_ANS'}, inplace=True)
    
    #join atraves do REG_ANS:
    #obs: optei por usar o left, ja que a tabela importante é a de balanço financeiro, mantive ela e trouxe
    #as info correspondentes
    dfJoin = pd.merge(df1, df2, on="REG_ANS", how="left")
    
    #agrupar dados por Razao_Social e UF:
    dfJoin = (dfJoin.groupby(["Razao_Social", "UF"], as_index=False).agg({ "ValorDespesa": "sum"}))   
    
    #media, desvio padrao e outras estatisticas:
    # print(dfJoin["ValorDespesa"].describe())
    
    #ordenando atraves do valor da despesa:
    dfJoin = dfJoin.sort_values("ValorDespesa")
    dfJoin = dfJoin.reset_index(drop=True)
    print(dfJoin.tail())
    
    dfJoin.to_csv(f"data/arquivosDescomp/despesas_agregadas.csv", sep=";", index=False)
    
    
    
    
# df = pd.read_csv("data/arquivosDescomp/resultado_final.csv", sep=";")  
 
# joinCsv( df , "data/arquivosDescomp/Relatorio_cadop.csv")       
        
# consolidCsv("./data/arquivosDescomp")