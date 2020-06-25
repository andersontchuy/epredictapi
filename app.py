from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    data = 'PredictApp'
    
    return data

@app.route('/api-doc', methods=['GET'])
def show_doc():
    return render_template('document.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)