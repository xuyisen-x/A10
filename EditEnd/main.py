import erniebot.api_types
from flask import Flask, json, request, jsonify
from flask_cors import CORS

import erniebot
erniebot.api_type = 'aistudio'
erniebot.access_token = '72addf70fd5b019442eb523108ccac95f165a03c'

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

@app.route('/getpolish', methods=["GET", "POST"])
def getpolish():
    # 获取用户名
    username= request.form.get("user")
    # 获取用户的访问令牌
    key = request.form.get("key")
    # 获取用户提问内容
    quesCont = request.form.get("cont")
    # 在用户选中的文本前添加提问前缀
    askCont = "帮我润色下面这段话（请直接输出结果，不要在开头和结尾增加额外信息）:" + quesCont
    
    print(askCont)

    try:
        response = erniebot.ChatCompletion.create(
            model='ernie-3.5',
            messages=[{'role': 'user', 'content':askCont}],
        )
        resText = response['result']
        print(resText)
        webDict = {'answer': resText}
        return jsonify(webDict)
    except:
        return "error"
    
@app.route('/getabbreviate', methods=["GET", "POST"])
def getabbreviate():
    # 获取用户名
    username= request.form.get("user")
    # 获取用户的访问令牌
    key = request.form.get("key")
    # 获取用户提问内容
    quesCont = request.form.get("cont")
    askCont = "帮我缩写下面这段话（请直接输出结果，不要在开头和结尾增加额外信息）:" + quesCont
    
    print(askCont)

    try:
        response = erniebot.ChatCompletion.create(
            model='ernie-3.5',
            messages=[{'role': 'user', 'content':askCont}],
        )
        resText = response['result']
        print(resText)
        webDict = {'answer': resText}
        return jsonify(webDict)
    except:
        return "error"
    
@app.route('/getexpand', methods=["GET", "POST"])
def getexpand():
    # 获取用户名
    username= request.form.get("user")
    # 获取用户的访问令牌
    key = request.form.get("key")
    # 获取用户提问内容
    quesCont = request.form.get("cont")
    askCont = "帮我扩写下面这段话（请直接输出结果，不要在开头和结尾增加额外信息）:" + quesCont
    
    print(askCont)

    try:
        response = erniebot.ChatCompletion.create(
            model='ernie-3.5',
            messages=[{'role': 'user', 'content':askCont}],
        )
        resText = response['result']
        print(resText)
        webDict = {'answer': resText}
        return jsonify(webDict)
    except:
        return "error"
    
@app.route('/getextend', methods=["GET", "POST"])
def getextend():
    # 获取用户名
    username= request.form.get("user")
    # 获取用户的访问令牌
    key = request.form.get("key")
    # 获取用户提问内容
    quesCont = request.form.get("cont")
    askCont = "帮我续写下面这段话（请直接输出结果，不要在开头和结尾增加额外信息）:" + quesCont
    
    print(askCont)

    try:
        response = erniebot.ChatCompletion.create(
            model='ernie-3.5',
            messages=[{'role': 'user', 'content':askCont}],
        )
        resText = response['result']
        print(resText)
        webDict = {'answer': resText}
        return jsonify(webDict)
    except:
        return "error"
    
@app.route('/getOCR', methods=["GET", "POST"])
def getOCR():
    # 获取用户名
    username= request.form.get("user")
    # 获取用户的访问令牌
    key = request.form.get("key")
    # 获取用户提问内容
    quesCont = request.form.get("cont")
    # 在用户选中的文本前添加提问前缀
    askCont = "帮我识别下面这张图片中的文字内容（请直接输出识别到的文字内容，不要在开头和结尾增加额外信息）:" + quesCont
    
    print(askCont)

    try:
        response = erniebot.ChatCompletion.create(
            model='ernie-3.5',
            # model = ?
            messages=[{'role': 'user', 'content':askCont}],
        )
        resText = response['result']
        print(resText)
        webDict = {'answer': resText}
        return jsonify(webDict)
    except:
        return "error"
    
@app.route('/getdescribe', methods=["GET", "POST"])
def getdescribe():
    # 获取用户名
    username= request.form.get("user")
    # 获取用户的访问令牌
    key = request.form.get("key")
    # 获取用户提问内容
    quesCont = request.form.get("cont")
    # 在用户选中的文本前添加提问前缀
    askCont = "帮我描述下面这幅图片的内容（请直接输出结果，不要在开头和结尾增加额外信息）:" + quesCont
    
    print(askCont)

    try:
        response = erniebot.ChatCompletion.create(
            model='ernie-3.5',
            # model = ?
            messages=[{'role': 'user', 'content':askCont}],
        )
        resText = response['result']
        print(resText)
        webDict = {'answer': resText}
        return jsonify(webDict)
    except:
        return "error"

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
