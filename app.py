from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, root_mean_squared_error
from scipy import stats
import joblib
import os

app = Flask(__name__)

# Train and save the model once on startup
def train_model():
    np.random.seed(42)
    n = 50
    
    data = {
        "Engine_Size": np.random.uniform(1.0, 4.5, n),
        "Horsepower": np.random.randint(70, 300, n),
        "Age": np.random.randint(1, 15, n),
        "Mileage": np.random.randint(10000, 200000, n),
        "Brand_Value": np.random.randint(1, 5, n)
    }
    
    df = pd.DataFrame(data)
    df["Price"] = (
        df["Engine_Size"] * 500000 +
        df["Horsepower"] * 10000 -
        df["Age"] * 80000 -
        df["Mileage"] * 5 +
        df["Brand_Value"] * 300000
    )
    
    # Feature scaling
    feature_cols = ["Engine_Size", "Horsepower", "Age", "Mileage", "Brand_Value"]
    df_scaled = df.copy()
    df_scaled[feature_cols] = (df[feature_cols] - df[feature_cols].min()) / (df[feature_cols].max() - df[feature_cols].min())
    
    # Train model
    X = df_scaled[feature_cols]
    y = df["Price"]
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Save model and scaler info
    joblib.dump(model, 'model.pkl')
    scaler_info = {
        'min': df[feature_cols].min().to_dict(),
        'max': df[feature_cols].max().to_dict()
    }
    joblib.dump(scaler_info, 'scaler_info.pkl')
    
    return model, scaler_info

# Load or train model
if os.path.exists('model.pkl'):
    model = joblib.load('model.pkl')
    scaler_info = joblib.load('scaler_info.pkl')
else:
    model, scaler_info = train_model()

def detect_data_type(value):
    """Predict the type of input value"""
    try:
        # Try to convert to integer
        if '.' not in str(value) and value.isdigit():
            return {"type": "Integer", "value": int(value)}
        
        # Try to convert to float
        try:
            float_val = float(value)
            return {"type": "Float/Decimal", "value": float_val}
        except ValueError:
            pass
        
        # Check if it's a date
        from datetime import datetime
        date_formats = ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%d/%m/%Y"]
        for fmt in date_formats:
            try:
                datetime.strptime(value, fmt)
                return {"type": "Date", "value": value}
            except ValueError:
                pass
        
        # Check if it's boolean
        if value.lower() in ['true', 'false', 'yes', 'no']:
            return {"type": "Boolean", "value": value.lower() in ['true', 'yes']}
        
        # Otherwise it's text
        return {"type": "String/Text", "value": value}
    
    except Exception as e:
        return {"type": "Unknown", "value": str(value), "error": str(e)}

def predict_price(engine_size, horsepower, age, mileage, brand_value):
    """Predict car price using trained model"""
    try:
        engine_size = float(engine_size)
        horsepower = float(horsepower)
        age = float(age)
        mileage = float(mileage)
        brand_value = float(brand_value)
        
        # Scale features
        features = np.array([[engine_size, horsepower, age, mileage, brand_value]])
        feature_cols = ["Engine_Size", "Horsepower", "Age", "Mileage", "Brand_Value"]
        
        for i, col in enumerate(feature_cols):
            features[0, i] = (features[0, i] - scaler_info['min'][col]) / (scaler_info['max'][col] - scaler_info['min'][col])
        
        # Predict
        predicted_price = model.predict(features)[0]
        return {"predicted_price": round(predicted_price, 2), "success": True}
    
    except Exception as e:
        return {"error": str(e), "success": False}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/detect-type', methods=['POST'])
def api_detect_type():
    data = request.json
    user_input = data.get('input', '')
    result = detect_data_type(user_input)
    return jsonify(result)

@app.route('/api/predict-price', methods=['POST'])
def api_predict_price():
    data = request.json
    result = predict_price(
        data.get('engine_size'),
        data.get('horsepower'),
        data.get('age'),
        data.get('mileage'),
        data.get('brand_value')
    )
    return jsonify(result)

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """Analyze multiple inputs - detect types and optionally predict price"""
    data = request.json
    inputs = data.get('inputs', [])
    predict = data.get('predict', False)
    
    results = {
        "detected_types": [detect_data_type(inp) for inp in inputs],
        "price_prediction": None
    }
    
    if predict and len(inputs) >= 5:
        results["price_prediction"] = predict_price(*inputs[:5])
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
