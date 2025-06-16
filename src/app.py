import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fetch_nutrition import load_nutrition_data, get_nutrition
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
import io

# Load nutrition data
df = load_nutrition_data()

# Load MobileNetV2 model
model = MobileNetV2(weights='imagenet')

# Title and intro
st.title("🍽️ NutriPlate - Indian Food Nutrition Estimator")

# Upload an image
uploaded_file = st.file_uploader("Upload an image of your food:", type=["jpg", "jpeg", "png"])

selected_quantities = {}
predicted_foods = []

if uploaded_file:
    img = image.load_img(uploaded_file, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_batch = np.expand_dims(img_array, axis=0)
    img_preprocessed = preprocess_input(img_batch)

    # Predict using MobileNetV2
    preds = model.predict(img_preprocessed)
    decoded_preds = decode_predictions(preds, top=3)[0]

    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    st.subheader("🔍 Top Predictions:")

    for pred in decoded_preds:
        label = pred[1].replace("_", " ").title()
        confidence = round(pred[2] * 100, 2)
        st.write(f"{label} ({confidence}%)")
        # Only keep food that matches Indian names from dataset
        for dish in df['Food']:
            if label.lower() in dish.lower() or dish.lower() in label.lower():
                predicted_foods.append(dish)

if predicted_foods:
    st.subheader("🍛 Confirm and Enter Quantities:")
    for food in predicted_foods:
        qty = st.number_input(f"Enter quantity for {food} (servings):", min_value=0.0, value=1.0, step=0.5)
        if qty > 0:
            selected_quantities[food] = qty

# If user manually selects from full list (optional fallback)
st.subheader("📋 Or Select from Full Menu")
with st.expander("Choose food items manually"):
    for food in df['Food']:
        qty = st.number_input(f"{food} (servings):", min_value=0.0, value=0.0, step=0.5, key=food)
        if qty > 0:
            selected_quantities[food] = qty

# Show nutrition breakdown
if selected_quantities:
    result_df, totals = get_nutrition(selected_quantities, df)

    st.subheader("🔍 Nutrition Breakdown")
    st.dataframe(result_df.set_index('Food'))

    st.markdown(f"**Total Calories:** {totals['Calories_kcal']} kcal")
    st.markdown(f"**Total Protein:** {totals['Protein_g']} g")
    st.markdown(f"**Total Fat:** {totals['Fat_g']} g")
    st.markdown(f"**Total Carbs:** {totals['Carbs_g']} g")

    # Pie chart
    fig, ax = plt.subplots()
    ax.pie([
        totals['Protein_g'],
        totals['Fat_g'],
        totals['Carbs_g']
    ], labels=['Protein', 'Fat', 'Carbs'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)
