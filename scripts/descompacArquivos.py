import zipfile
import os

zipados = os.listdir("./data")

def descompactar():
    caminhos = []
    for arquivo in zipados:
        if arquivo.endswith(".zip"):
            caminho = os.path.join("data", arquivo)
            caminhos.append(caminho)
            with zipfile.ZipFile(caminho, 'r') as zip_ref:
                zip_ref.extractall("data/arquivosDescomp")
                
    
    return caminhos