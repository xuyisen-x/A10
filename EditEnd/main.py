import erniebot.api_types
from flask import Flask, json, request, jsonify
from flask_cors import CORS

import requests
import base64

import erniebot
erniebot.api_type = 'aistudio'
erniebot.access_token = '864047b2b8503537bd38de6b97c719cec8f911cd'


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
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    access_token = '24.d77e9c375cc2a6291df9e6e69f202960.2592000.1723340824.282335-93707685'

    # img = base64.b64encode(quesCont)
    # img_base64 = base64.b64encode(quesCont).decode('utf-8')
    params = {"image": quesCont}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    
    response = requests.post(request_url, data=params, headers=headers)
    
    if response.status_code == 200:  # 检查响应状态码是否为200
        return response.json()
    else:
        print(f"请求失败，状态码：{response.status_code}")
        return None


    
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
            # 将model替换为多模态小模型
            messages=[{'role': 'user', 'content':askCont}],
        )
        resText = response['result']
        print(resText)
        webDict = {'answer': resText}
        return jsonify(webDict)
    except:
        return "error"

@app.route('/getobjectdetection', methods=["GET", "POST"])
def getobjectdetection():
    # 获取用户名
    username= request.form.get("user")
    # 获取用户的访问令牌
    key = request.form.get("key")
    # 获取用户提问内容
    quesCont = request.form.get("cont")
    # 在用户选中的文本前添加提问前缀
    askCont = "帮我识别下面这幅图片中的主要目标对象（请直接输出结果，不要在开头和结尾增加额外信息）:" + quesCont
    
    print(askCont)

    try:
        response = erniebot.ChatCompletion.create(
            model='ernie-3.5',
            # 将model替换为多模态小模型
            messages=[{'role': 'user', 'content':askCont}],
        )
        resText = response['result']
        print(resText)
        webDict = {'answer': resText}
        return jsonify(webDict)
    except:
        return "error"

@app.route('/getaudiorecognition', methods=["GET", "POST"])
def getaudiorecognition():
    # 获取用户名
    username= request.form.get("user")
    # 获取用户的访问令牌
    key = request.form.get("key")
    # 获取用户提问内容
    quesCont = request.form.get("cont")
    # 在用户选中的文本前添加提问前缀
    askCont = "帮我识别下面这段音频中的内容并转换为文字输出（请直接输出结果，不要在开头和结尾增加额外信息）:" + quesCont
    
    print(askCont)

    try:
        response = erniebot.ChatCompletion.create(
            model='ernie-3.5',
            # 将model替换为多模态小模型
            messages=[{'role': 'user', 'content':askCont}],
        )
        resText = response['result']
        print(resText)
        webDict = {'answer': resText}
        return jsonify(webDict)
    except:
        return "error"

@app.route('/getvideosummary', methods=["GET", "POST"])
def getvideosummary():
    # 获取用户名
    username= request.form.get("user")
    # 获取用户的访问令牌
    key = request.form.get("key")
    # 获取用户提问内容
    quesCont = request.form.get("cont")
    # 在用户选中的文本前添加提问前缀
    askCont = "帮我对下面这段视频的主要内容进行总结（请直接输出结果，不要在开头和结尾增加额外信息）:" + quesCont
    
    print(askCont)

    try:
        response = erniebot.ChatCompletion.create(
            model='ernie-3.5',
            # 将model替换为多模态小模型
            messages=[{'role': 'user', 'content':askCont}],
        )
        resText = response['result']
        print(resText)
        webDict = {'answer': resText}
        return jsonify(webDict)
    except:
        return "error"
    
@app.route('/getimagegeneration', methods=["GET", "POST"])
def getimagegeneration():
    # 获取用户名
    username= request.form.get("user")
    # 获取用户的访问令牌
    key = request.form.get("key")
    # 获取用户提问内容
    quesCont = request.form.get("cont")
    askCont = "帮我依据下面的文本提示生成图片（请直接输出结果，不要在开头和结尾增加额外信息）:" + quesCont
    
    print(askCont)

    try:
        response = erniebot.ChatCompletion.create(
            model='ernie-vilg-v2',
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
