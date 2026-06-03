import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from scipy import stats

# ── visual settings ───────────────────────────────────────────────────────────

# colors by income level (World Bank standard)
color_by_income = {
    "HIGH INCOME":"#1a6faf",
    "UPPER MIDDLE INCOME":"#e07b30",
    "LOWER MIDDLE INCOME":"#2ca02c",
    "LOW INCOME":"#d62728",
}

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 150,
})


# ── helper functions ──────────────────────────────────────────────────────────

#draws the trend line and returns R²
def regression_line(ax, x, y):
    
    mask = ~(np.isnan(x) | np.isnan(y))
    x_clean, y_clean = x[mask], y[mask]

    slope, intercept, r, p_value, _ = stats.linregress(x_clean, y_clean)

    x_line = np.linspace(x_clean.min(), x_clean.max(), 200)
    ax.plot(x_line, intercept + slope * x_line, color="black", lw=1.2, ls="--")

    return r, r**2, p_value

# plots points colored by income level and country name
def scatter_with_labels(ax, df, col_x, col_y):

    df_clean = df.dropna(subset=[col_x, col_y])

    for _, row in df_clean.iterrows():
        color = color_by_income.get(row["Income"], "#999999")
        ax.scatter(row[col_x], row[col_y], color=color, s=45, zorder=3,
                   edgecolors="white", linewidths=0.5)
        ax.annotate(
            row["Country Name"],
            xy=(row[col_x], row[col_y]),
            xytext=(0, 5),              # offset 5 points upward
            textcoords="offset points",
            fontsize=5.5,
            ha="center",
            color="#444444",
        )


def income_legend(ax):

    handles = [
        plt.Line2D([0], [0], marker="o", color="w",
                   markerfacecolor=color, markersize=7, label=name.title())
        for name, color in color_by_income.items()
    ]
    ax.legend(handles=handles, fontsize=7, framealpha=0.8, loc="best")


def stats_box(ax, r, r2, p_value):

    # format p value: show exact value or < 0.001
    p_str = f"{p_value:.3f}" if p_value >= 0.001 else "< 0.001"
    text = f"r = {r:.3f}\nR² = {r2:.3f}\np = {p_str}"
    ax.text(
        0.97, 0.05, text,
        transform = ax.transAxes,
        fontsize = 7.5,
        va = "bottom", ha = "right",
        bbox = dict(boxstyle = "round, pad = 0.4", facecolor = "white", edgecolor = "#cccccc")
    )


def save_fig(fig, path):
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


# ── analysis plots ────────────────────────────────────────────────────────────

def plot_analysis1(df, region, fig_num, output_path):
    """
    analysis 1 - investment and income
    x axis: average investment rate (% of GDP)
    y axis: most recent GDP per capita PPP
    """
    data = df.dropna(subset=["investment_avg", "gdp_latest"])

    fig, ax = plt.subplots(figsize=(8, 5.5))
    scatter_with_labels(ax, data, "investment_avg", "gdp_latest")
    r, r2, p = regression_line(ax, data["investment_avg"].values, data["gdp_latest"].values)

    ax.set_xlabel("Average Investment Rate – Gross Capital Formation (% of GDP) | 1990–2024")
    ax.set_ylabel("GDP per Capita, PPP (current int. $) | Most recent year")
    ax.set_title(
        f"FIGURE {fig_num} – Investment and Income per Capita\n{region.title()} | R² = {r2:.3f}",
        fontweight="bold", pad=10
    )
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    income_legend(ax)
    stats_box(ax, r, r2, p)
    save_fig(fig, output_path)
    return r, r2, p


def plot_analysis2(df, region, fig_num, output_path):
    """
    analysis 2 – income convergence
    x axis: constant GDP per capita PPP in 1990
    y axis: average GDP per capita growth 1990–2017
    """
    data = df.dropna(subset=["gdp_1990", "gdp_growth_avg"])

    fig, ax = plt.subplots(figsize=(8, 5.5))
    scatter_with_labels(ax, data, "gdp_1990", "gdp_growth_avg")
    r, r2, p = regression_line(ax, data["gdp_1990"].values, data["gdp_growth_avg"].values)

    ax.set_xlabel("GDP per Capita, PPP (constant 2021 int. $) | Base year: 1990")
    ax.set_ylabel("Average GDP per Capita Growth (% p.a.) | 1990–2017")
    ax.set_title(
        f"FIGURE {fig_num} – Income Convergence\n{region.title()} | R² = {r2:.3f}",
        fontweight="bold", pad=10
    )
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    income_legend(ax)
    stats_box(ax, r, r2, p)
    save_fig(fig, output_path)
    return r, r2, p


def plot_analysis3(df, region, fig_num, output_path):
    """
    analysis 3 – population growth and income
    x axis: average population growth (%)
    y axis: most recent GDP per capita PPP
    """
    data = df.dropna(subset=["pop_growth_avg", "gdp_latest"])

    fig, ax = plt.subplots(figsize=(8, 5.5))
    scatter_with_labels(ax, data, "pop_growth_avg", "gdp_latest")
    r, r2, p = regression_line(ax, data["pop_growth_avg"].values, data["gdp_latest"].values)

    ax.set_xlabel("Average Population Growth (% p.a.) | 1990–2024")
    ax.set_ylabel("GDP per Capita, PPP (current int. $) | Most recent year")
    ax.set_title(
        f"FIGURE {fig_num} – Population Growth and Income per Capita\n{region.title()} | R² = {r2:.3f}",
        fontweight="bold", pad=10
    )
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    income_legend(ax)
    stats_box(ax, r, r2, p)
    save_fig(fig, output_path)
    return r, r2, p
