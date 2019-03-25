from flask import Flask, request, jsonify
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
client = MongoClient('localhost', port=27017)
db = client.test

@app.route('/api/auth/login', methods=['POST'])
def login():
    r = request.get_json()
    
    user = db.users.find_one({ "username": r["username"] })
    if user is None:
        return jsonify({
            "auth": False,
            "message": "Username or password is incorrect."
        })
    
    if bcrypt.checkpw(r["password"].encode('utf-8'), user['password'].encode('utf-8')):
        return jsonify({
            "auth": True,
            "message": "Username or password was correct."
        })
    else:
        return jsonify({
            "auth": False,
            "message": "Username or password is incorrect."
        })
