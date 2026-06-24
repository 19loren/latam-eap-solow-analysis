# Solow Model – World Bank Analysis

Integrative Project | Macroeconomics III · Economic Statistics  
School of Economics and Business — Economics

---

## Objective

Evaluate whether the **Solow Model** can explain countries’ economic performance,
using World Bank data (1990–2024).

Three analyses are carried out for **two geographic groupings**:

|#| Analysis | X Variable | Y Variable | Reference |
|-|------|----------------|----------------|---------|
|1| Investment and Income | Gross Capital Formation (% GDP) – 1990–2024 average | GDP per capita PPP (current) | Mankiw Fig. 8-6 |
|2| Income Convergence | GDP per capita PPP, constant – 1999 | Average GDP per capita growth – 1990–2017 | Blanchard Fig. 10.2|
|3| Population Growth and Income | Average population growth – 1990–2024 | GDP per capita PPP (current) | Mankiw Fig. 8-13 |

---

## Project Structure

```
solow_analysis/
├── data/
│   └── world_data.xlsx          # World Bank dataset
├── src/
│   ├── data_loader.py           # Data loading preprocessing
│   ├── plots.py                 # Chart generation (ABNT standart)
│   └── main.py                  # Main script
├── outputs/
│   ├── figures/                 # Generated charts (PNG)
│   └── tables/                  # Correlation table (CSV)
├── requirements.txt
└── README.md
```
---

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run anaysis

```bash
python src/main.py
```

## Data

Source: [World Data – World Development Indicators](https://data.worldbank.org/indicator)

| Variable | Code (ID) |
|----------|-------------|
| GDP per capita, PPP (current international $) | `NY.GDP.PCAP.PP.CD` |
| Gross Capital Formation (% of GDP) | `NE.GDI.TOTL.ZS` |
| GDP per capita growth (anual %) | `NY.GDP.PCAP.KD.ZG` |
| GDP per capita, PPP (constant 2021 international $) | `NY.GDP.PCAP.PP.KD` |
| Populational Growth (anual %) | `SP.POP.GROW` |

---

## Outputs

- **6 charts** (`outputs/figures/`) — named `fig01_analysis1_latam.png`, etc.
- **Correlation table** (`outputs/tables/correlation_summary.csv`) with R² per analysis and region.

---

## Dependencies

See `requirements.txt`. Main ones: `pandas`, `matplotlib`, `scipy`, `adjustText`.
