import streamlit as st
import pickle
import json
import numpy as np


page_bg = """
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://www.sobha.com/blog/wp-content/uploads/2022/12/luxury-apartments-in-bangalore-for-sale-top-image-Sobha-Arena-1.png");
background-size: cover;
}
[data-testid="stHeader"] {
background-color : rgba(0,0,0,0);
}
</style>
"""
st.markdown(page_bg,unsafe_allow_html=True)

# Function to load saved artifacts
def load_saved_artifacts():
    global __data_columns
    global __locations
    global __model

    with open("./columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk

    if __model is None:  # Check if __model is None
        with open('./banglore_home_prices_model.pickle', 'rb') as f:
            __model = pickle.load(f)

# Function to get estimated price
def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)

# Function to get location names
def get_location_names():
    return __locations

__model = None

load_saved_artifacts()

st.markdown(
    """
    <style>
    .title-container {
        padding: 20px;
        border: 2px solid #333333;
        border-radius: 10px;
        margin-bottom: 20px;
        background-color: rgba(240, 240, 240, 0.8);
        display: flex;
        justify-content: center; /* Align horizontally in center */
        align-items: center; /* Align vertically in center */
    }
    .title-text {
        font-size: 36px;
        font-weight: bold;
        color: #333333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="title-container">
        <p class="title-text">Bangalore House Price Prediction</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar for user input
st.sidebar.header("Enter Details")
total_sqft = st.sidebar.number_input("Total Square Feet", min_value=100, max_value=10000, step=100)
bhk = st.sidebar.number_input("Number of Bedrooms (BHK)", min_value=1, max_value=10, step=1)
bath = st.sidebar.number_input("Number of Bathrooms", min_value=1, max_value=10, step=1)
location = st.sidebar.selectbox("Location", get_location_names())

# Predict button
if st.sidebar.button("Predict"):
    estimated_price = get_estimated_price(location, total_sqft, bhk, bath)
    st.markdown(
        """
        <style>
        .success-container {
            padding: 20px;
            border: 2px solid #28A745; /* Change border color here */
            border-radius: 10px;
            margin-bottom: 20px;
            background-color: rgba(212, 237, 218, 0.8); /* Change background color here */
            display: flex;
            justify-content: center; /* Align horizontally in center */
            align-items: center; /* Align vertically in center */
        }
        .success-text {
            font-size: 18px;
            font-weight: bold;
            color: #333333;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Display success message with estimated price inside the styled container
    st.markdown(
        """
        <div class="success-container">
            <p class="success-text">Estimated Price for a {bhk} BHK House in {location}: ₹ {estimated_price:.2f} Lakhs</p>
        </div>
        """.format(bhk=bhk, location=location, estimated_price=estimated_price),
        unsafe_allow_html=True
    )
