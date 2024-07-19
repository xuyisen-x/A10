# 环境变量设置
import os
os.environ["EB_AGENT_ACCESS_TOKEN"] = "72addf70fd5b019442eb523108ccac95f165a03c"
import io
from PIL import Image


# 用于异步处理
import threading
import asyncio
class RunThread(threading.Thread):
    def __init__(self, func, args, kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = None
        super().__init__()

    def run(self):
        self.result = asyncio.run(self.func(*self.args, **self.kwargs))

def run_async(func, *args, **kwargs):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    if loop and loop.is_running():
        thread = RunThread(func, args, kwargs)
        thread.start()
        thread.join()
        return thread.result
    else:
        return asyncio.run(func(*args, **kwargs))

# flask后端框架
from flask import Flask, json, request, jsonify, stream_with_context, Response
from flask_cors import CORS

# 文心大模型所需要
import erniebot
import erniebot.api_types
erniebot.api_type = 'aistudio'
erniebot.access_token = '72addf70fd5b019442eb523108ccac95f165a03c'
# 后期考虑本地部署，不使用API
from erniebot_agent.tools import RemoteToolkit #用于翻译、文本识别
from erniebot_agent.file import GlobalFileManagerHandler
trans_tool = RemoteToolkit.from_aistudio("translation").get_tools()[0]
asr_tool = RemoteToolkit.from_aistudio("asr").get_tools()[0]

#OCR所需要
from paddleocr import PaddleOCR, draw_ocr
ocr = PaddleOCR(use_angle_cls=True, lang="ch")

#通用包
import cv2
import numpy as np

# 公式识别所需
from pix2tex.cli import LatexOCR
latexOCRModel = LatexOCR()

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resource={r'/*': {'origins': '*'}})

def generate_stream(response_stream):
    """A generator function to yield data from the response stream."""
    try:
        for chunk in response_stream:
            yield chunk.get_result()
    except Exception as e:
        yield "￥￥￥出现错误，请重试￥￥￥"

def ask(askCont):
    try:
        response_stream = erniebot.ChatCompletion.create(
            model='ernie-4.0-turbo-8k',
            messages=[{'role': 'user', 'content':askCont}],
            stream=True,
        )
        return Response(stream_with_context(
            generate_stream(response_stream)
            ))
    except:
        return "error"
    
def checkUser(username, key):
    # TO DO
    return True

@app.route('/adduser', methods=['get', 'post'])
def adduser():
    username = request.form.get("username")
    password = request.form.get("password")
    print(username)
    print(password)
    return "已接收用户信息"

@app.route('/getpolish', methods=["GET", "POST"])
def getpolish():
    username= request.form.get("user")
    key = request.form.get("key")
    if not checkUser(username, key):
        return "permission denied"
    quesCont = request.form.get("cont")
    askCont = "帮我润色下面这段话（请直接输出结果，不要在开头和结尾增加额外信息），我的信息是使用markdown给出的，请尽量使用markdown语法:" + quesCont
    return ask(askCont)
    
@app.route('/getabbreviate', methods=["GET", "POST"])
def getabbreviate():
    username= request.form.get("user")
    key = request.form.get("key")
    if not checkUser(username, key):
        return "permission denied"
    quesCont = request.form.get("cont")
    askCont = "帮我缩写下面这段话（请直接输出结果，不要在开头和结尾增加额外信息），我的信息是使用markdown给出的，请尽量使用markdown语法:" + quesCont
    return ask(askCont)
    
@app.route('/getexpand', methods=["GET", "POST"])
def getexpand():
    username= request.form.get("user")
    key = request.form.get("key")
    if not checkUser(username, key):
        return "permission denied"
    quesCont = request.form.get("cont")
    askCont = "帮我扩写下面这段话（请直接输出结果，不要在开头和结尾增加额外信息），我的信息是使用markdown给出的，请尽量使用markdown语法:" + quesCont
    return ask(askCont)
    
@app.route('/getextend', methods=["GET", "POST"])
def getextend():
    username= request.form.get("user")
    key = request.form.get("key")
    if not checkUser(username, key):
        return "permission denied"
    quesCont = request.form.get("cont")
    askCont = "帮我续写下面这段话（请直接输出结果，不要在开头和结尾增加额外信息），我的信息是使用markdown给出的，请尽量使用markdown语法:" + quesCont
    return ask(askCont)

# 将dataUrl转换为openCV格式的图片
def dataUrl2Img(dataUrl:str):
    import base64
    import urllib.parse
    # 检查是否是Base64编码
    if ";base64," in dataUrl:
        header, encoded = dataUrl.split(";base64,", 1)
        # 解码Base64数据
        image_data = base64.b64decode(encoded)
    else:
        header, encoded = dataUrl.split(",", 1)
        # 解码URL编码数据
        image_data = urllib.parse.unquote_to_bytes(encoded)

    nparr = np.frombuffer(image_data, np.uint8)
    # 使用OpenCV将NumPy数组转换为图像
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image

def dataUrl2ImgPIL(dataUrl:str):
    import base64
    import urllib.parse
    # 检查是否是Base64编码
    if ";base64," in dataUrl:
        header, encoded = dataUrl.split(";base64,", 1)
        # 解码Base64数据
        image_data = base64.b64decode(encoded)
    else:
        header, encoded = dataUrl.split(",", 1)
        # 解码URL编码数据
        image_data = urllib.parse.unquote_to_bytes(encoded)

    img = Image.open(io.BytesIO(image_data))
    # 使用OpenCV将NumPy数组转换为图像
    return img

@app.route('/ocr', methods=["GET", "POST"])
def dataUrl2Str():
    dataUrl = request.form.get("dataurl")
    result = ocr.ocr(dataUrl2Img(dataUrl), cls=True)
    resultStr = ""
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            resultStr += "<p>" + line[1][0] + "</p>"
    tempMap = {'string':resultStr}
    return jsonify(tempMap)

@app.route('/formula', methods=["GET", "POST"])
def dataUrl2Formula():
    dataUrl = request.form.get("dataurl")
    result = latexOCRModel(dataUrl2ImgPIL(dataUrl))
    resultStr = "<p>$" + result + "$</p>"
    tempMap = {'string':resultStr}
    return jsonify(tempMap)

async def trans_async(to,query):
    result = await trans_tool(to=to,q=query)
    return result

@app.route('/translate', methods=["GET", "POST"])
def translate():
    query = request.form.get("q")
    to = request.form.get("to")
    result = run_async(trans_async,to,query)['result']['trans_result']
    resultStr = []
    for idx in range(len(result)):
        res = result[idx]
        resultStr.append(res['dst'])
    tempMap = {'string':resultStr}
    return jsonify(tempMap)

async def asr_async(dataBase64, format):
    import base64
    file_manager = GlobalFileManagerHandler().get()
    local_file = await file_manager.create_file_from_bytes(file_contents=base64.b64decode(dataBase64), filename="temp")
    return await asr_tool(format=format, speech=local_file.id)

@app.route('/asr', methods=["GET", "POST"])
def asr():
    dataUrl = request.form.get("dataurl")
    header, dataBase64 = dataUrl.split(";base64,", 1)
    if header == "data:audio/vnd.wave":
        format = "wav"
    elif header == "data:application/octet-stream":
        format = "pcm"
    elif header == "data:audio/amr":
        format = "amr"
    elif header == "data:audio/mp4":
        format = "m4a"
    else:
        resultMap = {'string':'此格式暂不支持'}
        return jsonify(resultMap)
    tempMap = run_async(asr_async,dataBase64,format)
    if tempMap['err_no'] != 0:
        resultMap = {'string':tempMap['err_msg']}
    else:
        resultMap = {'string':tempMap['result'][0]}
    return jsonify(resultMap)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)