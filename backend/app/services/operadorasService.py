import csv
from pathlib import Path
import pandas as pd



infoOperadoras = Path("C:/Users/Juan/Desktop/TesteTecnicoIntuitive/data/arquivosDescomp/Relatorio_cadop.csv")

despesasConsolidadas = Path("C:/Users/Juan/Desktop/TesteTecnicoIntuitive/data/arquivosDescomp/resultado_final.csv")

despesasAgregadas = "C:/Users/Juan/Desktop/TesteTecnicoIntuitive/data/arquivosDescomp/despesas_agregadas.csv"


def buscarCNPJ(cnpj: str):
    with open(infoOperadoras, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")

        for row in reader:
            if row["CNPJ"] == cnpj:
                return {
                    "cnpj": row["CNPJ"],
                    "razao_social": row["Razao_Social"],
                    "nome_fantasia": row["Nome_Fantasia"],
                    "modalidade": row["Modalidade"],
                    "uf": row["UF"]
                }

    return None

def buscarDespesas(cnpj: str):
    registroOperado = None
    
    with open(infoOperadoras, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        
        for row in reader:
            if row["CNPJ"] == cnpj:
                registroOperado = row["REGISTRO_OPERADORA"]
                break
    
    despesas = []      
    #agora vou procurar atraves do registro q salvei vou procurar no outro csv:
    with open(despesasConsolidadas, newline="", encoding="utf-8") as csvfile:
        reader2 = csv.DictReader(csvfile, delimiter=";")
    
        
        for row in reader2:
            if row["REG_ANS"] == registroOperado:
            
                despesas.append({
                    "ano": int(row["ANO"]),
                    "trimestre": int(row["TRISMESTRE"]),
                    "descricao": row["DESCRICAO"],
                    "valor": float(row["ValorDespesa"])
        })
    return despesas

def buscarDespesasUF(uf: str):
    df = pd.read_csv(despesasAgregadas, sep=";")
    df_filtrado = df[df["UF"] == uf]
    despesas = df_filtrado["ValorDespesa"].sum()
    return despesas
    
    
    
    
    
def listarOperadoras(cursor: int | None = None, limit: int = 5):
    #importante fazer um sorte aqui pra deixar na ordem
    df = pd.read_csv("C:/Users/Juan/Desktop/TesteTecnicoIntuitive/data/arquivosDescomp/despesas_agregadas.csv", sep=";")
    #vou criar um id aqui, para poder fazer keyset pagination
    df = df.reset_index()  
    df = df.rename(columns={"index": "id"})

    #cursos é o registro da ultima coluna que mostra na pagina
    if cursor:
        #pegamos todos depois dele
        df = df[df["id"] > cursor]

    #pegamos o depois do cursor até o limite
    df_pag = df.head(limit)

    #definimos o proximo cursos - caso n seja o ultimo
    next_cursor = df_pag["id"].iloc[-1] if not df_pag.empty else None

    #pegamos os registros dos itens
    
    items = [
        str(row["Razao_Social"]) for _, row in df_pag.iterrows()
    ]

    return {"items": items, "next_cursor": next_cursor}
    

    