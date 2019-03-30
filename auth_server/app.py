#!/usr/bin/env python3
from flask import Flask, request
from auth_server.controller import send_code, verify_code

app = Flask(__name__)


@app.route('/login', methods=['GET'])
def login():
    user = request.args.get("username")
    return send_code(user)


@app.route('/auth', methods=['GET'])
def auth():
    username = request.args.get("username")
    code = request.args.get("code")
    return verify_code(username, code)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
