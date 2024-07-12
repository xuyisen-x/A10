import erniebot.api_types
from flask import Flask, json, request, jsonify
from flask_cors import CORS

import time
import requests
import base64
# 小模型统一调度access_token
# (Access token默认有效期为30天）from 2024.7.12 to 2024.8.11
access_token = '24.2700356a8fe52a6966ff99ff340232e0.2592000.1723386112.282335-93882240'

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

    params = {
        "image": quesCont
    }
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    
    response = requests.post(request_url, data=params, headers=headers)

    if response.status_code == 200:  # 检查响应状态码是否为200
        json_response = response.json()
        if 'words_result' in json_response:
            words_list = [result['words'] for result in json_response['words_result']]
            combined_text = ' '.join(words_list)
            return combined_text
        else:
            return "No words found in the response"
    else:
        return f"Request failed with status code: {response.status_code}"

@app.route('/getdescribe', methods=["POST"])
def getdescribe():
        # 获取用户名
    username= request.form.get("user")
    # 获取用户的访问令牌
    key = request.form.get("key")
    # 获取请求体
    request_data = request.get_json()
    
    # 获取图片数据
    image_data = request_data.get("image")
    
    # 构造请求 URL
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/image-understanding/request"
    request_url = f"{request_url}?access_token={access_token}"
    
    # 构造请求体
    params = {
        "image": image_data,
        "question": "这张图片里有什么？",
        "output_CHN": True
    }
    
    headers = {'Content-Type': 'application/json'}
    
    # 发送请求
    response = requests.post(request_url, json=params, headers=headers)

    if response.status_code == 200:
        json_response = response.json()
        if 'result' in json_response and 'task_id' in json_response['result']:
            task_id = json_response['result']['task_id']
            
            # 构造获取结果的请求
            result_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/image-understanding/get-result"
            result_url = f"{result_url}?access_token={access_token}"
            
            result_params = {"task_id": task_id}
            
            # 循环获取结果，直到处理完成
            while True:
                result_response = requests.post(result_url, json=result_params, headers=headers)
                result_json = result_response.json()
                
                if result_json['result']['ret_code'] == 0:
                    return result_json['result']['description']
                elif result_json['result']['ret_code'] != 1:  # 如果不是处理中，就是出错了
                    return f"Error: {result_json['result']['ret_msg']}"
                
                time.sleep(1)  # 等待1秒后再次请求
        else:
            return "No task ID found in the response"
    else:
        return f"Request failed with status code: {response.status_code}"
    

@app.route('/getobjectdetection', methods=["POST"])
def getobjectdetection():
        # 获取用户名
    username= request.form.get("user")
    # 获取用户的访问令牌
    key = request.form.get("key")
    # 获取请求体
    request_data = request.get_json()
    
    # 获取图片数据
    image_data = request_data.get("image")
    
    # 构造请求 URL
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/image-understanding/request"
    request_url = f"{request_url}?access_token={access_token}"
    
    # 构造请求体
    params = {
        "image": image_data,
        "question": "你现在是一个高级计算机视觉专家,专门从事目标检测任务。我需要你基于图像内容理解API的输出,执行精确的目标检测任务。",
        "output_CHN": True
    }
    
    headers = {'Content-Type': 'application/json'}
    
    # 发送请求
    response = requests.post(request_url, json=params, headers=headers)

    if response.status_code == 200:
        json_response = response.json()
        if 'result' in json_response and 'task_id' in json_response['result']:
            task_id = json_response['result']['task_id']
            
            # 构造获取结果的请求
            result_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/image-understanding/get-result"
            result_url = f"{result_url}?access_token={access_token}"
            
            result_params = {"task_id": task_id}
            
            # 循环获取结果，直到处理完成
            while True:
                result_response = requests.post(result_url, json=result_params, headers=headers)
                result_json = result_response.json()
                
                if result_json['result']['ret_code'] == 0:
                    return result_json['result']['description']
                elif result_json['result']['ret_code'] != 1:  # 如果不是处理中，就是出错了
                    return f"Error: {result_json['result']['ret_msg']}"
                
                time.sleep(1)  # 等待1秒后再次请求
        else:
            return "No task ID found in the response"
    else:
        return f"Request failed with status code: {response.status_code}"

@app.route('/getaudiorecognition', methods=["POST"])
def getaudiorecognition():
    # Get parameters from the request
    user = request.form.get('user')
    key = request.form.get('key')
    audio_data = request.files.get('audio').read()


    # Prepare the request body
    body = {
        "format": "pcm",
        "rate": 16000,
        "channel": 1,
        "cuid": "your_unique_device_id",
        "token": access_token,
        "speech": base64.b64encode(audio_data).decode(),
        "len": len(audio_data),
        "dev_pid": 1537  # For Mandarin with punctuation
    }

    # Make the API request
    api_url = 'http://vop.baidu.com/server_api'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_url, json=body, headers=headers)

    return jsonify(response.json())

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
