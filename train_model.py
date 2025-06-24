import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def train_and_save_model():
    # Load data
    data = pd.read_csv("C:/Users/DELL/Desktop/Price_Agriculture_commodities_Week.csv")  # Path to your CSV file

    # Handling Missing Data
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].median())

    categorical_columns = data.select_dtypes(exclude=[np.number]).columns
    for col in categorical_columns:
        data[col] = data[col].fillna(data[col].mode()[0])

    # Encoding Categorical Columns
    label_encoders = {}
    categorical_columns = ['State', 'District', 'Market', 'Commodity', 'Variety', 'Grade']
    for col in categorical_columns:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])
        label_encoders[col] = le  # Save the label encoder to inverse transform later

    # Date Feature Engineering
    data['Arrival_Date'] = pd.to_datetime(data['Arrival_Date'], format='%d-%m-%Y')
    data['Year'] = data['Arrival_Date'].dt.year
    data['Month'] = data['Arrival_Date'].dt.month
    data['Day'] = data['Arrival_Date'].dt.day
    data.drop(columns=['Arrival_Date'], inplace=True)

    # Feature Selection
    X = data.drop(columns=['Min Price', 'Max Price', 'Modal Price'])
    y = data['Modal Price']

    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the RandomForest model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions and evaluate
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Absolute Error: {mae}")
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")

    # Save the Model and Label Encoders
    with open('crop_price_model.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)

    with open('label_encoders.pkl', 'wb') as le_file:
        pickle.dump(label_encoders, le_file)

    print("✅ Model and Label Encoders saved successfully!")

if __name__ == "__main__":
    train_and_save_model()
