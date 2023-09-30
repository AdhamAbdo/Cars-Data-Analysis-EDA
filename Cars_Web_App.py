import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib


# Display the image
image_path = "Car_Analysissdsdedf.png"  # Update this with the correct path
st.image(image_path, caption='Car Analysis', use_column_width=True)

# Sidebar with input features
st.sidebar.title('Input Features')

# Sample data to set the dropdown options
make_options = ['Acura', 'Audi', 'BMW', 'Buick', 'Cadillac', 'Chevrolet',
                'Chrysler', 'Dodge', 'Ford', 'GMC', 'Honda', 'Hummer', 'Hyundai',
                'Infiniti', 'Isuzu', 'Jaguar', 'Jeep', 'Kia', 'Land Rover',
                'Lexus', 'Lincoln', 'MINI', 'Mazda', 'Mercedes-Benz', 'Mercury',
                'Mitsubishi', 'Nissan', 'Oldsmobile', 'Pontiac', 'Porsche', 'Saab',
                'Saturn', 'Scion', 'Subaru', 'Suzuki', 'Toyota', 'Volkswagen',
                'Volvo']

type_options = ['SUV', 'Sedan', 'Sports', 'Wagon', 'Truck', 'Hybrid']

origin_options = ['Asia', 'Europe', 'USA']

drivetrain_options = ['All', 'Front', 'Rear']

# Function to preprocess input data
def preprocess_input(data):
    data = pd.get_dummies(data, columns=["Make", "Type", "Origin", "DriveTrain"])
    return data

# Modified function to preprocess input data and apply one-hot encoding
def preprocess_input(data):
    # Create a DataFrame with the user inputs
    user_inputs_df = pd.DataFrame(data, index=[0])
    
    # One-hot encode the categorical features
    user_inputs_encoded = pd.get_dummies(user_inputs_df, columns=["Make", "Type", "Origin", "DriveTrain"])
    
    # Ensure the one-hot encoded DataFrame has all required columns
    # Initialize missing columns with zeros
    for col in ['Make_' + make for make in make_options] + \
               ['Type_' + type_ for type_ in type_options] + \
               ['Origin_' + origin for origin in origin_options] + \
               ['DriveTrain_' + drivetrain for drivetrain in drivetrain_options]:
        if col not in user_inputs_encoded.columns:
            user_inputs_encoded[col] = 0
    
    # Drop the original categorical columns    
    return user_inputs_encoded

# Modified function to predict MSRP with one-hot encoded features
def predict_msrp(features):
    model = LinearRegression()
    train_data_features = pd.read_csv('X_train.csv')
    train_data_target = pd.read_csv('y_train.csv')
    model.fit(train_data_features, train_data_target)
    
    # Preprocess the input features with one-hot encoding
    preprocessed_features = preprocess_input(features)
    
    # Ensure the input features match the model's expected columns
    expected_columns = train_data_features.columns
    for col in expected_columns:
        if col not in preprocessed_features.columns:
            preprocessed_features[col] = 0
    
    # Reorder columns to match the model's expected order
    preprocessed_features = preprocessed_features[expected_columns]
    
    # Predict the MSRP
    prediction = model.predict(preprocessed_features)[0]
    return prediction

# Streamlit app code remains the same


# Streamlit app
st.title('Car MSRP Prediction')

# Sidebar with input features
st.sidebar.title('Input Features')

# Collect user inputs for each feature
make = st.sidebar.selectbox('Make', make_options)
type_ = st.sidebar.selectbox('Type', type_options)
origin = st.sidebar.selectbox('Origin', origin_options)
drivetrain = st.sidebar.selectbox('DriveTrain', drivetrain_options)

# Other numerical features
engine_size = st.sidebar.number_input('EngineSize', min_value=0)
cylinders = st.sidebar.number_input('Cylinders', min_value=0)
horsepower = st.sidebar.number_input('Horsepower', min_value=0)
mpg_city = st.sidebar.number_input('MPG_City', min_value=0)
mpg_highway = st.sidebar.number_input('MPG_Highway', min_value=0)
weight = st.sidebar.number_input('Weight', min_value=0)
wheelbase = st.sidebar.number_input('Wheelbase', min_value=0)
length = st.sidebar.number_input('Length', min_value=0)

# Create a dictionary for input features
user_inputs = {
    'Make': make,
    'Type': type_,
    'Origin': origin,
    'DriveTrain': drivetrain,
    'EngineSize': engine_size,
    'Cylinders': cylinders,
    'Horsepower': horsepower,
    'MPG_City': mpg_city,
    'MPG_Highway': mpg_highway,
    'Weight': weight,
    'Wheelbase': wheelbase,
    'Length': length
}

# Predict MSRP when the user clicks a button
if st.button('Predict MSRP'):
    # Convert the user inputs to a DataFrame
    input_df = pd.DataFrame([user_inputs])
    
    # Predict the MSRP
    predicted_msrp = predict_msrp(input_df)
    
    # Display the predicted MSRP
    st.write('Predicted MSRP:', abs(predicted_msrp))
