# 3Data Cleaner & Value Type Predictor

A Flask-based web application that detects data types and predicts car prices using machine learning.

## Features

✨ **3 Main Features:**

1. **Data Type Detection** - Automatically detect if input is Integer, Float, Date, String, Boolean, etc.
2. **Car Price Prediction** - Input car features (Engine Size, Horsepower, Age, Mileage, Brand Value) to predict price
3. **Batch Analysis** - Analyze multiple values at once and optionally predict prices

## Project Structure

```
├── app.py                      # Flask backend with ML model
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html             # Main web interface
├── static/
│   ├── css/
│   │   └── style.css          # Website styling
│   └── js/
│       └── script.js          # Frontend logic
├── ml/
│   └── 3dataclean_andmodeltrain.py  # Original ML training script
├── model.pkl                  # Trained ML model (auto-generated)
└── scaler_info.pkl            # Scaling parameters (auto-generated)
```

## Installation

1. **Clone/Navigate to the project:**
   ```bash
   cd Pandas-and-numpy-ML-Project.worktrees/agents-three-data-cleaner-prediction
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Usage

### Tab 1: Type Detection
- Enter any value (number, text, date, etc.)
- Click "Detect Type" to see what type the system predicts
- Supports: Integer, Float, Date, String, Boolean

### Tab 2: Price Prediction
- Fill in car features:
  - Engine Size (1.0-4.5 liters)
  - Horsepower (70-300)
  - Age (1-15 years)
  - Mileage (10,000-200,000 km)
  - Brand Value (1-5 scale)
- Click "Predict Price" to get the estimated car price

### Tab 3: Batch Analysis
- Enter multiple values separated by commas or newlines
- Optionally check "Also predict price" to use the first 5 values for price prediction
- Analyze all values at once and see their detected types

## API Endpoints

### 1. Detect Data Type
```
POST /api/detect-type
Body: { "input": "value_to_detect" }
Response: { "type": "detected_type", "value": "parsed_value" }
```

### 2. Predict Car Price
```
POST /api/predict-price
Body: {
  "engine_size": 2.0,
  "horsepower": 150,
  "age": 5,
  "mileage": 50000,
  "brand_value": 4
}
Response: { "predicted_price": 1500000.00, "success": true }
```

### 3. Batch Analysis
```
POST /api/analyze
Body: {
  "inputs": ["value1", "value2", "value3"],
  "predict": true
}
Response: {
  "detected_types": [...],
  "price_prediction": {...}
}
```

## How It Works

### Data Type Detection
The system checks input values in this order:
1. **Integer** - Whole numbers without decimals
2. **Float** - Numbers with decimals
3. **Date** - Common date formats (YYYY-MM-DD, DD-MM-YYYY, etc.)
4. **Boolean** - true/false, yes/no values
5. **String** - Any other text value

### Price Prediction
- Uses a **Linear Regression** model trained on synthetic car data
- Training data includes 50 car samples with realistic price formulas
- Features are normalized (scaled) before prediction
- Model accuracy (R² score) is calculated on test data

## Technical Stack

- **Backend**: Flask (Python)
- **Machine Learning**: scikit-learn, pandas, numpy
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Data Processing**: scipy, pandas

## Features

- ✅ Real-time data type detection
- ✅ ML-based price prediction
- ✅ Responsive web design (works on mobile)
- ✅ Batch processing of multiple values
- ✅ Modern, clean UI with gradient design
- ✅ No external dependencies for frontend

## Requirements

- Python 3.8+
- Flask 2.3.2+
- pandas 2.0.3+
- scikit-learn 1.3.0+
- numpy 1.24.3+
- scipy 1.11.1+

## Notes

- The model is trained automatically on first run and cached as `model.pkl`
- All predictions are based on the trained linear regression model
- Date format detection supports multiple common formats
- For production use, consider using a proper WSGI server like Gunicorn

## Future Enhancements

- [ ] Support for CSV file uploads
- [ ] More advanced ML models (Random Forest, Gradient Boosting)
- [ ] Data visualization/charts
- [ ] Export results to CSV
- [ ] Historical predictions tracking
- [ ] More data type detections (phone numbers, emails, URLs)

## License

Open source - use freely for learning and projects

---

Built with ❤️ using Flask & Machine Learning | 3Data Cleaner . Making by Suresh Pun magar

# Car-Prediction-AI
