# container1/app.py
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

PERSISTENT_STORAGE_PATH = '../data'

@app.route('/store-file', methods=['POST'])
def store_file():
    data = request.get_json()

    # Validate JSON input
    if 'file' not in data or not data['file']:
        return jsonify({"file": None, "error": "Invalid JSON input."})

    file_name = data['file']
    file_data = data.get('data', '')

    file_path = os.path.join(PERSISTENT_STORAGE_PATH, file_name)

    try:
        with open(file_path, 'w') as file:
            file.write(file_data)
        return jsonify({"file": file_name, "message": "Success."})
    except Exception as e:
        return jsonify({"file": file_name, "error": "Error while storing the file to the storage."})

@app.route('/calculate', methods=['POST'])
def calculate():

    data = request.get_json()

    # Validate JSON input
    if 'file' not in data or data['file'] is None:
        return jsonify({"file": None, "error": "Invalid JSON input."})

    file_name = data['file']
    product = data.get('product', '')

    # Check if file exists
    file_path = os.path.join('../data', file_name)
    if not os.path.exists(file_path):
        return jsonify({"file": file_name, "error": "File not found."})

    # Send the request to Container 2
    response = requests.post('k8-assignment-container2-service:7000/sum', json={"file": file_name, "product": product})
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
