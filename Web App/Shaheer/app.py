from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # For now, just return a static prediction value
    prediction = 30000
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)
