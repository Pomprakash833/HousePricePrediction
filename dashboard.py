import streamlit as st
import pickle
import numpy as np

# Load model
with open("best_model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("🏠 Housing Price Prediction App")

st.write("Enter the house details below:")

# ------------------------------
# Numeric Inputs
# ------------------------------

area = st.number_input("Area (sq ft)", min_value=0, value=5000)
bedrooms = st.number_input("Bedrooms", min_value=1, value=3)
bathrooms = st.number_input("Bathrooms", min_value=1, value=2)
stories = st.number_input("Stories", min_value=1, value=1)
parking = st.number_input("Parking", min_value=0, value=1)

# ------------------------------
# Binary Yes/No Categorical Inputs
# Must convert to 1/0 for encoded columns
# ------------------------------

mainroad = st.selectbox("Mainroad access?", ["yes", "no"])
guestroom = st.selectbox("Guestroom?", ["yes", "no"])
basement = st.selectbox("Basement?", ["yes", "no"])
hotwaterheating = st.selectbox("Hot water heating?", ["yes", "no"])
airconditioning = st.selectbox("Air conditioning?", ["yes", "no"])
prefarea = st.selectbox("Preferred area?", ["yes", "no"])

# Convert yes/no to 1/0 for encoded columns
def bin_encode(x):
    return 1 if x == "yes" else 0

mainroad_yes = bin_encode(mainroad)
guestroom_yes = bin_encode(guestroom)
basement_yes = bin_encode(basement)
hotwaterheating_yes = bin_encode(hotwaterheating)
airconditioning_yes = bin_encode(airconditioning)
prefarea_yes = bin_encode(prefarea)

# ------------------------------
# Furnishing Status (encoded)
# 3 categories but model expects 2 dummy columns:
# semi-furnished → furnishingstatus_semi-furnished = 1
# unfurnished → furnishingstatus_unfurnished = 1
# furnished → both = 0
# ------------------------------

furnish = st.selectbox(
    "Furnishing Status",
    ["furnished", "semi-furnished", "unfurnished"]
)

furnishing_semi = 1 if furnish == "semi-furnished" else 0
furnishing_unf = 1 if furnish == "unfurnished" else 0

# ------------------------------
# Create input vector IN THE EXACT ORDER REQUIRED
# ------------------------------

X = np.array([[
    area,
    bedrooms,
    bathrooms,
    stories,
    parking,
    mainroad_yes,
    guestroom_yes,
    basement_yes,
    hotwaterheating_yes,
    airconditioning_yes,
    prefarea_yes,
    furnishing_semi,
    furnishing_unf
]])

# ------------------------------
# Predict Button
# ------------------------------

if st.button("Predict Price"):
    prediction = model.predict(X)
    st.success(f"🏡 Estimated Price: ₹{prediction[0]:,.2f}")
