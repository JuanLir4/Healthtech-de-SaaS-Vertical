import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

#a ideia é basicamente fazer web scraping para baixar esses dados

#lista os arquivos terminados em .zip    
def listarArquivos(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    links = soup.find_all("a")

    arquivos = []
    for l in links:
        href = l.get("href")
        if href.endswith(".zip"):
            arquivos.append(urljoin(url, href))

    return arquivos

#baixa o arquivo da url e salva na pasta data
def baixar(url, nome):
    r = requests.get(url)
    with open(f"data/{nome}", "wb") as f:
        f.write(r.content)
 

    
    