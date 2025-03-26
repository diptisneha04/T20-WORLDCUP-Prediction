import streamlit as st
import pickle
import pandas as pd

# Load the pre-trained pipeline that uses XGBoost
pipe = pickle.load(open('pipe.pkl', 'rb'))

# Define available teams and cities
teams = ['Australia', 'India', 'Bangladesh', 'New Zealand', 'South Africa', 
         'England', 'West Indies', 'Afghanistan', 'Pakistan', 'Sri Lanka']

cities = ['Colombo',
 'Mirpur',
 'Johannesburg',
 'Dubai',
 'Auckland',
 'Cape Town',
 'London',
 'Pallekele',
 'Barbados',
 'Sydney',
 'Melbourne',
 'Durban',
 'St Lucia',
 'Wellington',
 'Lauderhill',
 'Hamilton',
 'Centurion',
 'Manchester',
 'Abu Dhabi',
 'Mumbai',
 'Nottingham',
 'Southampton',
 'Mount Maunganui',
 'Chittagong',
 'Kolkata',
 'Lahore',
 'Delhi',
 'Nagpur',
 'Chandigarh',
 'Adelaide',
 'Bangalore',
 'St Kitts',
 'Cardiff',
 'Christchurch',
 'Trinidad']

# Streamlit app title
st.title('Cricket Score Predictor')

# Create columns for batting and bowling team selection
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select batting team', sorted(teams))
with col2:
    bowling_team = st.selectbox('Select bowling team', sorted(teams))

# City selection
city = st.selectbox('Select city', sorted(cities))

# Columns for input fields
col3, col4, col5 = st.columns(3)

with col3:
    current_score = st.number_input('Current Score', min_value=0)
with col4:
    overs = st.number_input('Overs done (works for overs > 5)', min_value=0.0, step=0.1)
with col5:
    wickets = st.number_input('Wickets out', min_value=0)

# Input for runs scored in the last 5 overs
last_five = st.number_input('Runs scored in last 5 overs', min_value=0)

# Prediction button
if st.button('Predict Score'):
    if overs <= 0:
        st.error("Please enter a valid number of overs (greater than 0).")
    else:
        balls_left = 120 - (overs * 6)
        wickets_left = 10 - wickets
        crr = current_score / overs  # Avoid division by zero; handled by the condition above

        # Create input DataFrame for prediction
        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [city],
            'current_score': [current_score],
            'balls_left': [balls_left],
            'wickets_left': [wickets_left],
            'crr': [crr],
            'last_five': [last_five]
        })

        # Make prediction
        result = pipe.predict(input_df)
        st.header("Predicted Score - " + str(int(result[0])))