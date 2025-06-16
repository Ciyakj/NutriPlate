import pandas as pd
import os

def load_nutrition_data():
    # Get path to the CSV file relative to this file
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, "data", "indian_foods.csv")
    return pd.read_csv(csv_path)

def get_nutrition(selected_quantities, df):
    result_rows = []
    for food, qty in selected_quantities.items():
        food_data = df[df['Food'] == food].squeeze()
        if not food_data.empty:
            calories = round(food_data['Calories'] * qty, 1)
            protein = round(food_data['Protein'] * qty, 1)
            fat = round(food_data['Fat'] * qty, 1)
            carbs = round(food_data['Carbs'] * qty, 1)
            result_rows.append({
                "Food": food,
                "Quantity": qty,
                "Calories": calories,
                "Protein": protein,
                "Fat": fat,
                "Carbs": carbs
            })
    return result_rows
