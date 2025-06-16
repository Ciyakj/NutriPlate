import streamlit as st
import matplotlib.pyplot as plt
from fetch_nutrition import load_nutrition_data, get_nutrition

# Load data
df = load_nutrition_data()

# Strip whitespace from column names
df.columns = df.columns.str.strip()

# App title
st.title("🍽️ NutriPlate - Indian Food Nutrition Estimator")

st.markdown("Select the food items on your plate with quantity (servings or grams):")

# List of food items
food_items = df['Food'].tolist()

# User input
selected_quantities = {}
for food in food_items:
    if st.checkbox(food):
        qty = st.number_input(f"Enter quantity for {food} (servings):", min_value=0.0, step=0.5, value=1.0)
        selected_quantities[food] = qty

# If user has selected items
if selected_quantities:
    st.subheader("🔍 Nutrition Breakdown")
    try:
        result_df, totals = get_nutrition(selected_quantities, df)
        st.dataframe(result_df)

        # Display total nutrition
        st.markdown(f"**Total Calories:** {totals['Calories_kcal']:.1f} kcal")
        st.markdown(f"**Total Protein:** {totals['Protein_g']:.1f} g")
        st.markdown(f"**Total Fat:** {totals['Fat_g']:.1f} g")
        st.markdown(f"**Total Carbs:** {totals['Carbs_g']:.1f} g")

        # Pie chart
        labels = ['Protein', 'Fat', 'Carbs']
        values = [totals['Protein_g'], totals['Fat_g'], totals['Carbs_g']]
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%')
        ax.set_title("Macronutrient Composition")
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Something went wrong during nutrition calculation: {e}")

else:
    st.info("Please select at least one food item.")
