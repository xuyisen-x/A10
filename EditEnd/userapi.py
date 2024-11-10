import mysql.connector as mysql # mysql-connector-python，用于连接MySQL数据库
from datetime import datetime
import uuid
from argon2 import PasswordHasher
import atexit

from flask import Blueprint, request, Response, jsonify, g, session
user_bp = Blueprint('user', __name__)

# 初始化密码哈希
ph = PasswordHasher()

# 数据库连接配置
db_config = {
    'host': 'rm-wz9o7k5a56910l3sffo.mysql.rds.aliyuncs.com',
    'user': '2183214655',
    'password': '2183214655',
    'database': 'spm'
}

def get_db():
    if 'db' not in g:
        print("connect db")
        g.db = mysql.connect(**db_config)
    return g.db

def checkUser(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT user_name FROM User WHERE user_name = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    return result is not None

def getUserPasswordHash(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM User WHERE user_name = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

# 注册用户
@user_bp.route('/adduser', methods=['POST'])
def adduser():
    username = request.form.get("username")
    password = request.form.get("password")

    # 检查用户名是否已存在
    if checkUser(username):
        return jsonify({'success': False, 'notes': '已经存在相同用户名的用户'})

    # 生成UUID作为user_id
    user_id = str(uuid.uuid4())

    # 使用Argon2加密密码
    password_hash = ph.hash(password)

    # 记录创建日期和最后活动日期
    create_date = datetime.now()
    last_active_date = create_date.strftime('%Y-%m-%d %H:%M:%S')

    # 插入新用户信息到数据库
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO User (user_id, user_name, password_hash, create_date, last_active_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, username, password_hash, create_date, last_active_date))
        conn.commit()
    except mysql.Error as e:
        conn.rollback()
        return jsonify({'success': False, 'notes': '数据库插入错误', 'error': str(e)})
    finally:
        cursor.close()

    return jsonify({'success': True, 'notes': '用户已成功注册'})

@user_bp.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if not checkUser(username):
        return jsonify({'success': False, 'notes': '用户名不存在'})

    # 获取数据库中的哈希密码
    password_hash = getUserPasswordHash(username)
    if password_hash is None:
        return jsonify({'success': False, 'notes': '未找到密码信息'})

    # 验证密码
    try:
        ph.verify(password_hash, password)
    except:
        return jsonify({'success': False, 'notes': '密码错误'})

    session['username'] = username
    # 如果验证通过，返回登录成功信息
    return jsonify({'success': True, 'notes': '登录成功'})

@user_bp.route('/loginasvisitor', methods=['POST'])
def loginasvisitor():
    if 'username' in session:
        # 删除已登录用户的session
        session.pop('username')
    return jsonify({'success': True, 'notes': '登录成功'})

@user_bp.route('/getusername', methods=['POST'])
def getusername():
    if 'username' in session:
        return jsonify({'success': True, 'username': session['username']})
    else:
        return jsonify({'success': False, 'notes': '未登录'})