import pandas as pd

def load_nutrition_data(csv_path="data/indian_foods.csv"):
    return pd.read_csv(csv_path)

def get_nutrition(selected_quantities, df):
    result_rows = []
    for food, qty in selected_quantities.items():
        row = df[df["Food"] == food].copy()
        if not row.empty:
            row.iloc[0, 1:] *= qty  # multiply all numeric columns by qty
            result_rows.append(row.iloc[0])
    result_df = pd.DataFrame(result_rows)
    total = result_df[["Calories_kcal", "Protein_g", "Fat_g", "Carbs_g"]].sum()
    return result_df, total
