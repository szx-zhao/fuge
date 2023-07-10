from flask import Flask, request
from flask_cors import CORS
from predict import predict_number
from flask import jsonify
from flask_jwt_extended import create_access_token
import os
import json
import re


app = Flask(__name__)
CORS(app)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    t = str(file)
    pattern = r"'([^']*)'"
    match = re.findall(pattern, t)
    if match:
        first_char = match[0]
    else:
        print("未找到匹配项")
        
    img_path = 'back-end/data/image/' + first_char
    predicted_number = predict_number(img_path)
    print('Predicted number:', predicted_number)
    return jsonify({'predicted_number': predicted_number.tolist()})



@app.route('/register', methods=['POST'])
def register():
    # Get the username and password from the request body
    data = request.get_json()
    username = data['username']
    password = data['password']
    # Debugging print statements
    print('Username:', username)
    print('Password:', password)
    # Write the data to a JSON file
    with open('./back-end/data/user.json', 'r') as f:
        user_data = json.load(f)
    view_list = user_data.get('view_list', [])
    view_list.append({'username': username, 'password': password})
    with open('./back-end/data/user.json', 'w') as f:
        json.dump({'view_list': view_list}, f)
    # Debugging print statement
    print('User data written to file')
    return 'Registration successful'

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('account')
    password = data.get('password')

    # read credentials from JSON file
    with open('./back-end/data/user.json') as f:
        credentials = json.load(f)['view_list']
        


    if any(c['username'] == username and c['password'] == password for c in credentials):
        
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})
    
@app.route('/logins', methods=['POST'])
def logins():
    data = request.get_json()
    username = data.get('account')
    password = data.get('password')
    # check user credentials and generate token
    access_token = create_access_token(identity=username)
    # send token as response
    return jsonify(access_token=access_token), 200

    
    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)



