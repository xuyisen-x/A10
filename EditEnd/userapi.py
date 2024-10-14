import mysql.connector as mysql # mysql-connector-python，用于连接MySQL数据库

from flask import Blueprint, request, Response, jsonify
user_bp = Blueprint('user', __name__)

def checkUser(username, key):
    # TO DO
    return True

# 注册用户
@user_bp.route('/adduser', methods=['get', 'post'])
def adduser():
    username = request.form.get("username")
    password = request.form.get("password")
    # TO DO
    print(username)
    print(password)
    return "已接收用户信息"