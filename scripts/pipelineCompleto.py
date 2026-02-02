from ingestaoApi import listarArquivos, baixar
from descompacArquivos import descompactar
from tratamentoCsv import joinCsv, consolidCsv

def executarPipeline(caminhoPasta, url):
    url = url = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2025/"

    for arquivo in listarArquivos(url):
        nome = arquivo.split("/")[-1]
        baixar(arquivo, nome)
        
    caminhos = descompactar()
    df = consolidCsv(caminhos, caminhoPasta)
    joinCsv(df, "data/arquivosDescomp/Relatorio_cadop.csv")
 
    
    
    


    