import pandas as pd
import pickle
import streamlit as st
from utils.db_connection import insert_crop_data, fetch_crop_data
from sklearn.preprocessing import LabelEncoder
# --- Frontend (Streamlit App) ---
def main():
    # Set page configuration
    st.set_page_config(page_title="🌾 Smart Agriculture App", page_icon="🌱", layout="centered")

    # Background Style with color and background image
    page_bg_img = '''
        <style>

        .stApp {
            background-image: url("https://images.unsplash.com/photo-1603190287605-6f8f73ff0b94?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            font-family: 'Segoe UI', sans-serif;
        }
        .stButton>button {
            background-color: #2e8b57;
            color: white;
            font-size: 18px;
            border-radius: 10px;
            padding: 10px 20px;
            margin-top: 10px;
        }
        .stButton>button:hover {
            background-color: #246b45;
        }
        .stTextInput>div>div>input, .stNumberInput>div>div>input, .stDateInput>div>div>input {
            border-radius: 8px;
            padding: 10px;
            background-color: rgba(255,255,255,0.9);
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #ffffff;
            text-shadow: 1px 1px 2px #000;
        }
        .block-container {
            background-color: rgba(255, 255, 255, 0.85);
            padding: 2rem;
            border-radius: 15px;
        }












        
        
        </style>
    '''

    # Load the model and label encoders
    try:
        model = pickle.load(open('crop_price_model.pkl', 'rb'))
        label_encoders = pickle.load(open('label_encoders.pkl', 'rb'))
    except FileNotFoundError:
        st.error("Model or label encoders not found. Please ensure they are saved and available.")
        return

    st.title("🌾 Smart Agriculture Crop Price Prediction")
    st.markdown("#### Enter the Crop Details Below:")

    # Input Fields
    col1, col2 = st.columns(2)

    with col1:
        state = st.text_input('State', 'Gujarat')
        district = st.text_input('District', 'Amreli')
        market = st.text_input('Market', 'Damnagar')
        commodity = st.text_input('Commodity', 'Cabbage')
        variety = st.text_input('Variety', 'FAQ')

    with col2:
        grade = st.text_input('Grade', 'FAQ')
        arrival_date = st.date_input('Arrival Date', pd.to_datetime('2023-07-27'))
        min_price = st.number_input('Min Price', min_value=0.0, format="%.2f")
        max_price = st.number_input('Max Price', min_value=0.0, format="%.2f")
        modal_price = st.number_input('Modal Price', min_value=0.0, format="%.2f")

    if st.button('Predict Crop Price'):
        try:
            # Prepare input data for prediction
            input_data = pd.DataFrame({
                'State': [state], 'District': [district], 'Market': [market],
                'Commodity': [commodity], 'Variety': [variety], 'Grade': [grade],
                'Arrival_Date': [arrival_date]
            })

            # Encode categorical columns, handle unseen labels gracefully
            for col in ['State', 'District', 'Market', 'Commodity', 'Variety', 'Grade']:
                if input_data[col][0] not in label_encoders[col].classes_:
                    st.warning(f"'{input_data[col][0]}' in column '{col}' was not seen during training. Handling as unknown.")
                    # Handle unseen labels by encoding them as -1 (or some other placeholder)
                    input_data[col] = -1
                else:
                    input_data[col] = label_encoders[col].transform(input_data[col])

            # Extract year, month, and day from arrival date
            input_data['Arrival_Date'] = pd.to_datetime(input_data['Arrival_Date'])
            input_data['Year'] = input_data['Arrival_Date'].dt.year
            input_data['Month'] = input_data['Arrival_Date'].dt.month
            input_data['Day'] = input_data['Arrival_Date'].dt.day
            input_data.drop(columns=['Arrival_Date'], inplace=True)

            # Make prediction
            prediction = model.predict(input_data)
            st.success(f"Predicted Modal Price: ₹ {prediction[0]:.2f}")

            # Insert data into the database
            insert_crop_data(state, district, market, commodity, variety, grade, arrival_date, min_price, max_price, prediction[0])
            st.success("✅ Data inserted successfully into the database!")

        except Exception as e:
            st.error(f"Something went wrong: {e}")

    # Show all entries from the database
    if st.button('Show Data from Database'):
        try:
            crops = fetch_crop_data()
            df = pd.DataFrame(crops, columns=['ID','State', 'District', 'Market', 'Commodity', 'Variety', 'Grade', 'Arrival Date', 'Min Price', 'Max Price', 'Modal Price'])
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error fetching data: {e}")

if __name__ == "__main__":
    main()
