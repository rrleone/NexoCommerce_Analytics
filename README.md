<div align="center">

<h1> NexoCommerce Analytics</h1>


### End-to-End Data Analytics & Business Intelligence

**E-Commerce · Sales Performance · Customer Behavior · Operations · Business Insights**

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"/>
  <img src="https://img.shields.io/badge/Power%20Query-217346?style=for-the-badge&logo=microsoftpowerpoint&logoColor=white"/>
  <img src="https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black"/>
  <img src="https://img.shields.io/badge/DAX-2C3E50?style=for-the-badge&logoColor=white"/>
</p>

**Transformando dados de e-commerce em indicadores, insights e decisões de negócio.**

</div>

---

## Visão geral do projeto

O **NexoCommerce Analytics** é um projeto de portfólio End-to-End de Análise de Dados e Business Intelligence, desenvolvido para simular uma operação de comércio eletrônico.

O projeto integra preparação, tratamento e validação de dados com Python, organização do modelo analítico e desenvolvimento de indicadores e dashboards interativos no Power BI.

A proposta é demonstrar como dados comerciais e operacionais podem ser transformados em informações gerenciais para acompanhamento de desempenho e apoio à tomada de decisão.

> **Projeto educacional:** os dados são sintéticos e não representam uma empresa real.

---

## Dashboard Power BI

O dashboard está organizado em três perspectivas complementares, permitindo explorar a operação sob diferentes dimensões.

### 01 — Visão Executiva

Acompanhamento dos principais indicadores de desempenho, incluindo faturamento, pedidos, itens vendidos e ticket médio, com análises comerciais e operacionais.

![Visão Executiva](05_Portfolio/01_VIS%C3%83O%20EXECUTIVA.png)

### 02 — Análise Comercial

Exploração do desempenho comercial por canal, categoria e produto, incluindo comparação de faturamento, volume e concentração de resultados.

![Análise Comercial](05_Portfolio/02_AN%C3%81LISE%20COMERCIAL.png)

### 03 — Operações e Produtos

Análise dos status dos pedidos e entregas, além de comparações entre categorias e produtos por volume.

![Operações e Produtos](05_Portfolio/03_OPERA%C3%87%C3%95ES%20E%20PRODUTOS.png)

---

## Problema de negócio e objetivos

Uma operação de comércio eletrônico precisa acompanhar simultaneamente resultados comerciais e desempenho operacional.

O projeto busca responder perguntas como:

- Qual é o faturamento e o volume de pedidos?
- Como se distribuem as vendas por canal?
- Quais categorias e produtos se destacam em faturamento ou volume?
- Como se comportam os pedidos e as entregas?
- Como evoluem os indicadores ao longo do tempo?
- Quais informações merecem atenção da gestão?

### Objetivos

- Organizar e validar dados de diferentes entidades.
- Desenvolver um processo estruturado de preparação de dados.
- Construir indicadores comerciais e operacionais.
- Explorar desempenho por canal, categoria e produto.
- Desenvolver um dashboard interativo.
- Comunicar resultados de forma clara e orientada ao negócio.

---

## Dados utilizados

O projeto utiliza dados sintéticos preparados para simular uma operação de e-commerce.

### Entidades

- Clientes
- Pedidos
- Itens de pedido
- Produtos
- Vendedores
- Pagamentos
- Entregas

### Organização dos dados

Os arquivos estão organizados em três grupos:

- **Originais:** dados de entrada.
- **Tratados:** dados preparados para análise.
- **Quarentena:** registros separados durante as verificações de qualidade.

Os dados são disponibilizados em formatos como CSV e JSON.

---

## Metodologia

**Dados → Profiling → Qualidade → ETL → Modelagem → DAX → Dashboard → Insights**

### 1. Data Profiling

Inspeção inicial da estrutura, conteúdo, tipos de dados e características dos arquivos.

### 2. Data Quality

Identificação e análise de registros inconsistentes, duplicidades, problemas de integridade e registros órfãos.

### 3. Data Cleaning & ETL

Preparação e tratamento dos dados por meio de scripts Python, organizando os conjuntos de dados para utilização analítica.

### 4. Data Validation

Validação dos arquivos tratados e verificação da consistência dos dados, com separação de registros que exigem análise adicional.

### 5. Data Modeling

Organização das tabelas e relacionamentos utilizados no modelo analítico do Power BI.

### 6. Business Metrics

Desenvolvimento de indicadores, medidas DAX, comparações mensais e textos dinâmicos de insights.

### 7. Business Analysis

Análise comercial, financeira, de produtos e operações, considerando o contexto dos filtros e indicadores.

### 8. Dashboard & Insights

Construção das páginas do dashboard e comunicação dos resultados por meio de indicadores e análises visuais.

---

## Tecnologias e ferramentas

| Tecnologia | Aplicação |
|---|---|
| **Python** | Tratamento e validação dos dados |
| **Pandas** | Manipulação e processamento |
| **CSV / JSON** | Arquivos de dados e mapeamentos |
| **Power Query** | Preparação dos dados no Power BI |
| **Power BI** | Modelagem, indicadores e dashboards |
| **DAX** | Medidas, KPIs e cálculos analíticos |
| **Git / GitHub** | Versionamento e documentação do projeto |

---

## Principais indicadores

O dashboard reúne indicadores para acompanhamento do desempenho comercial e operacional.

- **Faturamento**
- **Pedidos**
- **Itens vendidos**
- **Ticket médio**
- **Faturamento por canal**
- **Desempenho por categoria e produto**
- **Status dos pedidos**
- **Status e desempenho das entregas**
- **Variação mensal (MoM)**

Os valores exibidos dependem do contexto de filtros aplicado no relatório.

---

## Análises gerenciais

### Desempenho comercial

- Comparação de canais de venda.
- Análise de faturamento e volume.
- Desempenho de categorias e produtos.
- Concentração de faturamento.
- Ranking de produtos.

### Operações

- Distribuição dos status dos pedidos.
- Acompanhamento dos status das entregas.
- Análise de volume por categoria.
- Comparação de produtos por quantidade vendida.

### Insights dinâmicos

O dashboard utiliza textos dinâmicos para interpretar os dados conforme os filtros aplicados, buscando oferecer uma leitura gerencial além da simples apresentação dos valores.

As análises são descritivas e devem ser interpretadas dentro do escopo e das limitações dos dados sintéticos.

---

## Tratamento e validação dos dados

Os principais scripts do projeto são:

- `03_Scripts/01_etl_tratamento.py` — preparação e tratamento dos dados.
- `03_Scripts/02_validar_dados.py` — validação dos dados tratados.
- `03_Scripts/mapeamentos_sinteticos.json` — mapeamentos utilizados no projeto.
- `03_Scripts/requirements.txt` — dependências Python.
- `03_Scripts/README.md` — instruções para utilização dos scripts.

Os registros identificados como inconsistentes ou órfãos são separados em arquivos de quarentena para análise, evitando sua utilização automática no conjunto principal tratado.

---

## Estrutura do repositório

```text
NexoCommerce_Analytics/
│
├── 01_Dados/
│   ├── 01_Originais/
│   ├── 02_Tratados/
│   └── 03_Quarentena/
│
├── 02_PowerBI/
│   └── NexoCommerce_Analytics.pbix
│
├── 03_Scripts/
│   ├── 01_etl_tratamento.py
│   ├── 02_validar_dados.py
│   ├── mapeamentos_sinteticos.json
│   ├── requirements.txt
│   └── README.md
│
├── 04_Documentacao/
│   └── relatorio_validacao.csv
│
├── 05_Portfolio/
│   ├── 01_VISÃO EXECUTIVA.png
│   ├── 02_ANÁLISE COMERCIAL.png
│   └── 03_OPERAÇÕES E PRODUTOS.png
│
└── README.md
```

---

## Como explorar o projeto

1. Consulte `01_Dados/` para conhecer a organização dos arquivos.
2. Leia `03_Scripts/README.md` antes de executar os scripts.
3. Verifique os arquivos de dependências em `03_Scripts/requirements.txt`.
4. Consulte `04_Documentacao/relatorio_validacao.csv`.
5. Abra `02_PowerBI/NexoCommerce_Analytics.pbix` no Power BI Desktop.
6. Explore as três páginas do dashboard e interaja com os filtros.

> **Observação:** caminhos e configurações dos scripts podem exigir ajustes conforme o ambiente local.

---

## Limitações e premissas

- Os dados são sintéticos e possuem finalidade educacional e de portfólio.
- Os resultados não representam o desempenho de uma empresa real.
- As análises são descritivas e não comprovam relações de causa e efeito.
- Os indicadores dependem das regras de negócio e dos filtros aplicados.
- A execução dos scripts pode exigir ajustes nos caminhos locais.

---

## Conclusão

O NexoCommerce Analytics demonstra um fluxo de trabalho de Análise de Dados e Business Intelligence que integra preparação e validação de dados, tratamento com Python, modelagem, indicadores DAX e visualização no Power BI.

O projeto evidencia a importância de estruturar dados, validar informações e interpretar indicadores considerando o contexto do negócio.

O foco não está apenas na construção de dashboards, mas na capacidade de **transformar dados em informações úteis para análise e tomada de decisão**.

---

## Autor

**Renato Leone**  
Analista de Dados | Business Intelligence

- **GitHub:** [github.com/rrleone](https://github.com/rrleone)
- **Portfólio:** [Renato Leone — Data Analytics & BI](https://sites.google.com/view/renatoleone/)
- **Repositório:** [NexoCommerce Analytics](https://github.com/rrleone/NexoCommerce_Analytics)

## Referências

**Tecnologias e documentação**

- [Python](https://docs.python.org/3/)
- [Pandas](https://pandas.pydata.org/docs/)
- [Microsoft Power BI](https://learn.microsoft.com/power-bi/)
- [DAX — Microsoft Learn](https://learn.microsoft.com/dax/)

---

<div align="center">

**NEXOCOMMERCE ANALYTICS**

*Dados · Qualidade · Análise · Insights · Decisões*

**RENATO LEONE | DATA ANALYTICS & BUSINESS INTELLIGENCE**

</div>
