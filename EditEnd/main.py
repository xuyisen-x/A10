from flask import Flask, json, request, jsonify
from flask_cors import CORS
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resource={r'/*': {'origins': '*'}})

@app.route('/adduser', methods=['get', 'post'])
def adduser():
    username = request.form.get("username")
    password = request.form.get("password")
    print(username)
    print(password)
    return "已接收用户信息"

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
