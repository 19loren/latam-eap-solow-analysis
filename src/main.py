import os
import sys
import pandas as pd

# allows importing modules from the src folder
sys.path.insert(0, os.path.dirname(__file__))

from data_loader import load_data, calculate_averages, regions
from plots import plot_analysis1, plot_analysis2, plot_analysis3

# ── paths ─────────────────────────────────────────────────────────────────────
root_dir = os.path.join(os.path.dirname(__file__), "..")
data_file = os.path.join(root_dir, "data", "world_data.xlsx")
figures_dir = os.path.join(root_dir, "outputs", "figures")
tables_dir = os.path.join(root_dir, "outputs", "tables")

# maps analysis number to its chart function
charts = {
    1: plot_analysis1,
    2: plot_analysis2,
    3: plot_analysis3,
}


def main():
    os.makedirs(figures_dir, exist_ok=True)
    os.makedirs(tables_dir, exist_ok=True)

    print(f"Loading data: {data_file}\n")
    df_long = load_data(data_file)

    results = []  

    for idx, (region, slug) in enumerate(regions.items()):
        print(f"Region: {region}")
        df_countries = calculate_averages(df_long, region)
        print(f"  {len(df_countries)} countries with GDP data")

        for analysis_num, chart_fn in charts.items():
            # figures 1–3 for the 1st region, 4–6 for the 2nd
            fig_num  = idx * 3 + analysis_num
            filename = f"fig{fig_num:02d}_analysis{analysis_num}_{slug}.png"
            filepath = os.path.join(figures_dir, filename)

            r, r2, p = chart_fn(df_countries, region, fig_num, filepath)
            p_str = f"{p:.3f}" if p >= 0.001 else "< 0.001"
            print(f"  Figure {fig_num} (Analysis {analysis_num}) → {filename}  r={r:.3f}  R²={r2:.3f}  p={p_str}")

            results.append({
                "region": region,
                "analysis": analysis_num,
                "figure": fig_num,
                "filename": filename,
                "n_countries": len(df_countries),
                "r": round(r, 4),
                "r2": round(r2, 4),
                "p_value": round(p, 4),
            })

        print()

    
    table = pd.DataFrame(results)
    table_path = os.path.join(tables_dir, "correlations.csv")
    table.to_csv(table_path, index=False)
    print(f"Correlation table saved at: {table_path}")
    print(table.to_string(index=False))


if __name__ == "__main__":
    main()
