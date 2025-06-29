
# 🌾 Crop Price Prediction System

A machine learning-powered system that predicts crop prices using historical agricultural commodity data. This project includes data preprocessing, model training, and a web interface for making predictions.

## 📂 Project Structure

```
crop/
├── app.py                        
├── train_model.py                
├── crop_price_model.pkl          
├── label_encoders.pkl            
├── requirements.txt              
├── data/
│   └── Price_Agriculture_commodities_Week.csv   
├── utils/
│   └── db_connection.py          
└── .ipynb_checkpoints/           
```

## ⚙️ Features

- Predicts crop prices using historical data.
- Uses machine learning (e.g., regression models).
- Clean preprocessing and label encoding.
- Easy-to-use interface (likely via Flask or Streamlit).
- Organized file structure with modular scripts.

## 🛠️ Installation

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/crop-price-prediction.git
cd crop-price-prediction
```

2. **Create a virtual environment (optional but recommended):**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Run the application:**

```bash
python app.py
```

## 🧠 Model Training

To retrain the model with new data:

```bash
python train_model.py
```

Make sure to place your updated dataset in the `data/` folder and adjust the training script if needed.

## 📊 Dataset

The model uses weekly agricultural commodity prices from:

```
data/Price_Agriculture_commodities_Week.csv
```

Ensure this dataset is properly formatted with relevant features for accurate predictions.

## 📁 Requirements

Install the required Python packages:

```
Listed in requirements.txt
```
