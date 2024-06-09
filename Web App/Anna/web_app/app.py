from flask import Flask, request, render_template
import joblib
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

app = Flask(__name__)

# Define custom transformers
class LowerCaseTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        lowercase_func = np.vectorize(lambda s: s.lower() if isinstance(s, str) else s)
        X = lowercase_func(X)
        return X

class BoolToIntTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return X.astype(int)
    
# Load the trained model
model = joblib.load('../models/random_forest_model.joblib')

# List of luxury brands for the feature
luxury_brands = ['mercedes-benz', 'lexus', 'bmw', 'audi']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract form data
    brand = request.form['brand']
    model_car = request.form['model']
    year = int(request.form['year'])
    km = int(request.form['km'])
    steering_side = request.form['steering_side']
    region_specs = request.form['region_specs']
    
    # Create a DataFrame for the input
    data = pd.DataFrame({
        'brand': [brand],
        'model': [model_car],
        'year': [year],
        'km': [km],
        'steering_side': [steering_side],
        'region_specs': [region_specs]
    })

    # Feature engineering
    current_year = 2024
    data['car_age'] = current_year - data['year']
    data['warranty'] = False  # Default as False, change if necessary
    data['luxury'] = data['brand'].apply(lambda x: 1 if x.lower() in luxury_brands else 0)
    
    #print(data)
    # Predict the price
    prediction = model.predict(data)[0]
    
    return render_template('index.html', result=prediction)

if __name__ == '__main__':
    app.run(debug=True)
