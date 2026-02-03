# Documentação – Teste Técnico (SaaS Vertical)

##  Testes 1 e 2: 

Toda a implementação dos Testes 1 e 2 está localizada na pasta `script`. A execução completa pode ser feita rodando o arquivo:
`python pipelineCompleto.py`

### Descrição dos Arquivos

* **`pipelineCompleto.py`**: Arquivo principal do pipeline. Responsável por orquestrar todas as etapas dos Testes 1 e 2, chamando as funções na ordem correta.
* **`ingestaoAPI.py`**: Contém as funções responsáveis pela ingestão dos dados. Como os dados disponibilizados estavam acessíveis apenas por meio de uma página web, utilizei a abordagem de **web scraping** para realizar o download dos arquivos CSV, em vez do consumo direto de uma API.
* **`descompacArquivos.py`**: Arquivo usado para descompactar os arquivos `.zip`.
* **`tratamentoCsv.py`**: Responsável por todas as etapas de manipulação dos arquivos CSV, incluindo:
    * Consolidação dos arquivos e agrupamento de dados.
    * Tratamento e limpeza das informações.
    * Etapas finais do Teste 1 e todo o Teste 2.

> **Observação importante:** Os dados de despesas trimestrais não possuem uma coluna de CNPJ. Para resolver isso, realizei um **LEFT JOIN** utilizando o registro da operadora como chave. Optei pelo LEFT JOIN pois o objetivo principal é preservar todos os dados de despesas e apenas complementar com informações adicionais das operadoras.

*Os dados foram salvos na pasta `/data`.*

---

## Teste 3 – Banco de Dados e Análise

Para executar o Teste 3, os scripts SQL devem ser rodados na seguinte ordem:

1.  **`schema.sql`**: Responsável pela criação das tabelas finais do banco de dados. Optei por utilizar tabelas normalizadas e separadas, pois facilita manutenção e consistência, além de tornar as queries analíticas mais organizadas.
2.  **`staging.sql`**: Responsável pela criação das tabelas de staging e pela carga inicial dos arquivos CSV utilizando `COPY`.
3.  **`transform.sql`**: Responsável por transformar os dados das tabelas de staging e inseri-los nas tabelas finais. Optei por tratar e limpar os dados nessa etapa para manter as tabelas finais consistentes e confiáveis para análise.
4.  **`query.sql`**: Contém as queries analíticas solicitadas no teste.

---

##  Teste 4: API e Frontend

### Como rodar
* **Frontend:** `npm run dev` (dentro da pasta `frontend/frontend`)
* **Backend:** `uvicorn app.main:app` (dentro da pasta `backend`)

### Detalhes de Implementação
* **Backend:** Criei um servidor Python usando **FastAPI**, tecnologia que já tenho bastante afinidade. Dentro da pasta `backend` está toda a estrutura de API normalmente utilizada: rotas, models, services, etc.
    * **Paginação:** Usei **Keyset pagination**, que possui uma performance bem melhor. Como eu nunca tinha implementado, foi uma oportunidade muito boa de aprender.
    * **Estatísticas:** Usei a estratégia de **cachear resultados** a cada 10 minutos. Dessa forma, não é necessário recalcular a cada requisição e o sistema fica sólido a possíveis mudanças de dados.
* **Frontend:** Estou utilizando **Props/Events** simples por ser uma abordagem mais direta. Como esta foi a minha primeira vez mexendo com **Vue**, foquei em uma estrutura funcional e clara.

##### Obs: a coleção no Postman é o arquivo "testeTec.postman_collection.json"

---