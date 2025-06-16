import pandas as pd
import os

# Dynamically resolve the path to the CSV file
def load_nutrition_data(csv_path=os.path.join(os.path.dirname(__file__), "data", "indian_foods.csv")):
    return pd.read_csv(csv_path)

# Compute the nutrition breakdown based on selected items and quantities
def get_nutrition(selected_quantities, df):
    result_rows = []
    total = {
        'Calories_kcal': 0,
        'Protein_g': 0,
        'Fat_g': 0,
        'Carbs_g': 0
    }

    for food, qty in selected_quantities.items():
        item = df[df['Food'].str.lower() == food.lower()]
        if not item.empty:
            row = item.iloc[0]
            calories = row['Calories_kcal'] * qty
            protein = row['Protein_g'] * qty
            fat = row['Fat_g'] * qty
            carbs = row['Carbs_g'] * qty

            result_rows.append({
                'Food': food,
                'Quantity': qty,
                'Calories': round(calories, 1),
                'Protein': round(protein, 1),
                'Fat': round(fat, 1),
                'Carbs': round(carbs, 1)
            })

            total['Calories_kcal'] += calories
            total['Protein_g'] += protein
            total['Fat_g'] += fat
            total['Carbs_g'] += carbs

    # Round total values
    total = {k: round(v, 1) for k, v in total.items()}

    return result_rows, total
