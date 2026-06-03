# Solow Model – World Bank Analysis

Projeto Integrador | Macroeconomia III · Estatística Econômica  
Escola de Economia e Negócios — Ciências Econômicas

---

## Objetivo

Avaliar se o **Modelo de Solow** consegue explicar o desempenho econômico de países,
utilizando dados do Banco Mundial (1990–2024).

Três análises são realizadas para **dois recortes geográficos**:

| # | Análise | Variável X | Variável Y | Referência |
|---|---------|-----------|-----------|-----------|
| 1 | Investimento e Renda | Formação Bruta de Capital (% PIB) – média 1990–2024 | PIB per capita PPP (corrente) | Mankiw Fig. 8-6 |
| 2 | Convergência de Renda | PIB per capita PPP constante – 1990 | Crescimento médio PIB per capita – 1990–2017 | Blanchard Fig. 10.2 |
| 3 | Crescimento Populacional e Renda | Crescimento populacional médio – 1990–2024 | PIB per capita PPP (corrente) | Mankiw Fig. 8-13 |

---

## Estrutura do Projeto

```
solow_analysis/
├── data/
│   └── world_data.xlsx          # Base de dados do Banco Mundial
├── src/
│   ├── data_loader.py           # Carga e pré-processamento dos dados
│   ├── plots.py                 # Geração dos gráficos (ABNT)
│   └── main.py                  # Script principal — executa todas as análises
├── outputs/
│   ├── figures/                 # Gráficos gerados (PNG)
│   └── tables/                  # Tabela de correlações (CSV)
├── requirements.txt
└── README.md
```

---

## Como Executar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Rodar as análises (regiões padrão)

```bash
python src/main.py
```

### 3. Especificar regiões customizadas

```bash
python src/main.py --regions "LATIN AMERICA AND CARIBBEAN" "EAST ASIAN AND PACIFIC"
```

---

## Dados

Fonte: [Banco Mundial – World Development Indicators](https://data.worldbank.org/indicator)

| Variável | Código (ID) |
|----------|-------------|
| PIB per capita, PPP (current international $) | `NY.GDP.PCAP.PP.CD` |
| Formação Bruta de Capital (% do PIB) | `NE.GDI.TOTL.ZS` |
| Crescimento do PIB per capita (anual %) | `NY.GDP.PCAP.KD.ZG` |
| PIB per capita, PPP (constant 2021 international $) | `NY.GDP.PCAP.PP.KD` |
| Crescimento Populacional (anual %) | `SP.POP.GROW` |

---

## Outputs

- **6 gráficos** (`outputs/figures/`) — nomeados `fig01_analysis1_latam.png`, etc.
- **Tabela de correlações** (`outputs/tables/correlation_summary.csv`) com R² por análise e região.

---

## Dependências

Ver `requirements.txt`. Principais: `pandas`, `matplotlib`, `scipy`, `adjustText`.
