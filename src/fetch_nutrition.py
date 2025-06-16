import pandas as pd
import os

# Function to load the CSV with the correct path
def load_nutrition_data(csv_path=os.path.join(os.path.dirname(__file__), "data", "indian_foods.csv")):
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()  # Optional: strip any accidental spaces in column names
    return df

# Function to calculate nutrition based on selected food items and quantities
def get_nutrition(selected_quantities, df):
    result_rows = []

    for food, qty in selected_quantities.items():
        # Match food item
        food_data = df[df['Food'] == food].iloc[0]

        # Extract and scale nutritional values
        calories = round(food_data['Calories_kcal'] * qty, 1)
        protein = round(food_data['Protein_g'] * qty, 1)
        fat = round(food_data['Fat_g'] * qty, 1)
        carbs = round(food_data['Carbs_g'] * qty, 1)

        result_rows.append({
            "Food": food,
            "Quantity": qty,
            "Calories (kcal)": calories,
            "Protein (g)": protein,
            "Fat (g)": fat,
            "Carbs (g)": carbs
        })

    # Final DataFrame of selected food items
    result_df = pd.DataFrame(result_rows)

    # Totals
    totals = {
        "Total Calories (kcal)": result_df["Calories (kcal)"].sum(),
        "Total Protein (g)": result_df["Protein (g)"].sum(),
        "Total Fat (g)": result_df["Fat (g)"].sum(),
        "Total Carbs (g)": result_df["Carbs (g)"].sum()
    }

    return result_df, totals
