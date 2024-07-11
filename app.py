# # container1/app.py
# from flask import Flask, request, jsonify
# import requests
# import os

# app = Flask(__name__)

# PERSISTENT_STORAGE_PATH = '/judith_PV_dir'

# @app.route('/store-file', methods=['POST'])
# def store_file():
#     data = request.get_json()

#     # Validate JSON input
#     if 'file' not in data or not data['file']:
#         return jsonify({"file": None, "error": "Invalid JSON input."})

#     file_name = data['file']
#     file_data = data.get('data', '')

#     file_path = os.path.join(PERSISTENT_STORAGE_PATH, file_name)

#     try:
#         with open(file_path, 'w') as file:
#             file.write(file_data)
#         return jsonify({"file": file_name, "message": "Success."})
#     except Exception as e:
#         return jsonify({"file": file_name, "error": "Error while storing the file to the storage."})

# @app.route('/calculate', methods=['POST'])
# def calculate():

#     data = request.get_json()

#     # Validate JSON input
#     if 'file' not in data or data['file'] is None:
#         return jsonify({"file": None, "error": "Invalid JSON input."})

#     file_name = data['file']
#     product = data.get('product', '')

#     # Check if file exist
#     file_path = os.path.join('/judith_PV_dir', file_name)
#     if not os.path.exists(file_path):
#         return jsonify({"file": file_name, "error": "File not found."})

#     # Send the request to Container 2
#     response = requests.post('http://localhost:7000/sum', json={"file": file_name, "product": product})
#     return jsonify(response.json())

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=6000)

import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Endpoint for calculating sum of products from the file
@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        # check file is present or not and returns validation message
        if request.json["file"] == None:
            return {
                "file": None,
                "error": "Invalid JSON input."
            }
    except KeyError:
        return {
            "file": None,
            "error": "Invalid JSON input."
        }

    #check in the directory
    if not os.path.isfile("/judith_PV_dir/" + request.json["file"]):
        return {
            "file": request.json["file"],
            "error": "File not found."
        }

    # request is being forwarded to app2-service/sum
    response = requests.post(url="http://localhost:7000/sum", json=request.json, headers={'Content-Type': 'application/json'})
    return response.json()

# Endpoint for store file
@app.route("/store-file", methods=["POST"])
def store_file():
    try:
        # validations
        if request.json["file"] == None:
            return {
                "file": None,
                "error": "Invalid JSON input."
            }
    except KeyError:
        return {
            "file": None,
            "error": "Invalid JSON input."
        }

    try:
        # write the file data to the directory
        with open("/judith_PV_dir/" + request.json["file"], "w+") as csvfile:
            csvfile.write(request.json["data"].replace(" ", ""))

    except Exception as e:
        # file storage exception
        return {
            "file": None,
            "error": "Error while storing the file to the storage."
        }
   
    # success message
    return {
        "file": request.json["file"],
        "message": "Success."
    }

if __name__ == "__main__":
    app.json.sort_keys = False
    app.run(host="0.0.0.0", port=6000, debug=True)