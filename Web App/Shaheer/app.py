from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
from datetime import datetime

app = Flask(__name__)

# load models
luxury_model = joblib.load('models/luxury_model.pkl')
non_luxury_model = joblib.load('models/non_luxury_model.pkl')

luxury_brands = ['Lexus','Mercedes Benz','BMW','Audi']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Gather data from the form
    car_brand = request.form.get('brand')
    car_model = request.form.get('model')
    mileage = int(request.form.get('mileage'))
    model_year = int(request.form.get('year'))
    region_specs = request.form.get('specs')
    location = request.form.get('location')
    warranty = request.form.get('warranty') == 'True'
    service_history = request.form.get('history') == 'True'
    no_accidents = request.form.get('accidents') == 'True'

    # Create a DataFrame
    data = {
        'brand': [car_brand],
        'model': [car_model],
        'km': [mileage],
        'region_specs': [region_specs],
        'location_cleaned': [location],
        'warranty': [warranty],
        'service_hist': [service_history],
        'no_accident': [no_accidents],
        'luxury': [1 if car_brand in luxury_brands else 0],
        'age': [datetime.now().year - model_year]
    }
    df = pd.DataFrame(data)

    # Select the appropriate model
    if car_brand in luxury_brands:
        model = luxury_model
    else:
        model = non_luxury_model

    # Make a prediction
    prediction = model.predict(df)[0]
    prediction = round(prediction/500) * 500
    pred_lower = f"{prediction - 10000:,}"
    pred_higher = f"{prediction - 4000:,}"
    pred_range = pred_lower + ' - ' + pred_higher

    # Return the result as JSON
    return jsonify(prediction=pred_range)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=8080)