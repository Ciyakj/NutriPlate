import pandas as pd
import os

def load_nutrition_data(csv_path=os.path.join(os.path.dirname(__file__), "data", "indian_foods.csv")):
    return pd.read_csv(csv_path)

def get_nutrition(selected_quantities, df):
    result_rows = []
    totals = {"Calories_kcal": 0, "Protein_g": 0, "Fat_g": 0, "Carbs_g": 0}

    for food, qty in selected_quantities.items():
        food_data = df[df['Food'] == food].iloc[0]

        calories = round(food_data['Calories_kcal'] * qty, 1)
        protein = round(food_data['Protein_g'] * qty, 1)
        fat = round(food_data['Fat_g'] * qty, 1)
        carbs = round(food_data['Carbs_g'] * qty, 1)

        result_rows.append({
            "Food": food,
            "Quantity": qty,
            "Calories_kcal": calories,
            "Protein_g": protein,
            "Fat_g": fat,
            "Carbs_g": carbs,
        })

        totals["Calories_kcal"] += calories
        totals["Protein_g"] += protein
        totals["Fat_g"] += fat
        totals["Carbs_g"] += carbs

    result_df = pd.DataFrame(result_rows)
    return result_df, totals
