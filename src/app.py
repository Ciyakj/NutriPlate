import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fetch_nutrition import load_nutrition_data, get_nutrition

# ✅ Must be first Streamlit command
st.set_page_config(page_title="🍽️ NutriPlate - Indian Food Nutrition Estimator")

st.title("🍽️ NutriPlate - Indian Food Nutrition Estimator")
st.markdown("### Select the food items on your plate with quantity (servings or grams):")

# Load dataset
df = load_nutrition_data()

# Get user-selected foods
selected_items = st.multiselect("Select the food items on your plate:", df["Food"].tolist())

# Ask quantity for each selected food
selected_quantities = {}
for item in selected_items:
    qty = st.number_input(f"Enter quantity for {item} (servings):", min_value=0.0, step=0.5)
    if qty > 0:
        selected_quantities[item] = qty

# Show nutrition breakdown
if selected_quantities:
    st.subheader("🔍 Nutrition Breakdown")

    result_df, totals = get_nutrition(selected_quantities, df)

    for _, row in result_df.iterrows():
        qty = selected_quantities[row["Food"]]
        st.markdown(
            f"**{row['Food']} × {qty}**  \n"
            f"Calories: {row['Calories_kcal'] * qty:.1f} kcal | "
            f"Protein: {row['Protein_g'] * qty:.1f} g | "
            f"Fat: {row['Fat_g'] * qty:.1f} g | "
            f"Carbs: {row['Carbs_g'] * qty:.1f} g"
        )

    # 📊 Pie chart
    st.subheader("📊 Calorie Contribution by Food")
    fig, ax = plt.subplots()
    labels = result_df["Food"]
    sizes = [row['Calories_kcal'] * selected_quantities[row['Food']] for _, row in result_df.iterrows()]
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

    # 🧾 Total Nutrition
    st.subheader("🧾 Total Nutrition")
    st.markdown(f"**Calories:** {totals['Calories_kcal']:.1f} kcal")
    st.markdown(f"**Protein:** {totals['Protein_g']:.1f} g")
    st.markdown(f"**Fat:** {totals['Fat_g']:.1f} g")
    st.markdown(f"**Carbs:** {totals['Carbs_g']:.1f} g")
