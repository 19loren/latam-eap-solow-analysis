import pandas as pd

regions = {
    "LATIN AMERICA AND CARIBBEAN": "latam",
    "EAST ASIAN AND PACIFIC": "eap",
}

years = [f"{y} [YR{y}]" for y in range(1990, 2025)]


def load_data(excel_path):
    df = pd.read_excel(excel_path)

    fixed_cols = ["Country Name", "Country Code", "By Region", "Income", "Series Code"]
    year_cols  = [c for c in years if c in df.columns]
    df = df[fixed_cols + year_cols]

    # unpivot year columns into rows
    df = df.melt(
        id_vars=fixed_cols,
        value_vars=year_cols,
        var_name="year_str",
        value_name="value"
    )

    df["year"]  = df["year_str"].str.extract(r"(\d{4})").astype(int)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    return df.drop(columns="year_str")

# receives the long-format df and returnos one row per country with all summary variables needed
def calculate_averages(df, region):
    df = df[df["By Region"].str.upper() == region.upper()].copy()

    # ── world bank series codes ───────────────────────────────────────────────
    GDP_CURRENT = "NY.GDP.PCAP.PP.CD"  # GDP per capita PPP (current)
    INVESTMENT = "NE.GDI.TOTL.ZS"    # gross capital formation (% GDP)
    GDP_GROWTH = "NY.GDP.PCAP.KD.ZG" # GDP per capita growth (%) 
    GDP_CONSTANT = "NY.GDP.PCAP.PP.KD" # GDP per capita PPP (const. 2021)
    POP_GROWTH = "SP.POP.GROW"       # population growth (%)

    def series(code):
        return df[df["Series Code"] == code]

    # analyses 1 & 3 — most recent GDP per capita available
    gdp_latest = (
        series(GDP_CURRENT)
        .dropna(subset=["value"])
        .sort_values("year")
        .groupby(["Country Name", "Country Code", "Income"])
        .last()[["value"]]
        .rename(columns={"value": "gdp_latest"})
        .reset_index()
    )

    # analysis 1 — average investment rate over the full period
    investment_avg = (
        series(INVESTMENT)
        .dropna(subset=["value"])
        .groupby("Country Name")["value"]
        .mean()
        .rename("investment_avg")
    )

    # analysis 2 — average GDP per capita growth between 1990 and 2017
    gdp_growth_avg = (
        series(GDP_GROWTH)
        .query("1990 <= year <= 2017")
        .dropna(subset=["value"])
        .groupby("Country Name")["value"]
        .mean()
        .rename("gdp_growth_avg")
    )

    # analysis 2 — constant GDP per capita in 1990 (starting point)
    gdp_1990 = (
        series(GDP_CONSTANT)
        .query("year == 1990")
        .dropna(subset=["value"])
        .set_index("Country Name")["value"]
        .rename("gdp_1990")
    )

    # analysis 3 — average population growth over the full period
    pop_growth_avg = (
        series(POP_GROWTH)
        .dropna(subset=["value"])
        .groupby("Country Name")["value"]
        .mean()
        .rename("pop_growth_avg")
    )

    # merge everything into a single per-country df
    result = (
        gdp_latest
        .set_index("Country Name")
        .join(investment_avg)
        .join(gdp_growth_avg)
        .join(gdp_1990)
        .join(pop_growth_avg)
        .reset_index()
    )

    return result
