from flask import Blueprint, request, stream_with_context, Response, jsonify
ocr_asr_bp = Blueprint('ocr-asr', __name__)

# 环境变量设置
import os
os.environ["EB_AGENT_ACCESS_TOKEN"] = "72addf70fd5b019442eb523108ccac95f165a03c"
from erniebot_agent.tools import RemoteToolkit #用于翻译、文本识别
from erniebot_agent.file import GlobalFileManagerHandler
import erniebot_agent
trans_tool = RemoteToolkit.from_aistudio("translation").get_tools()[0]
asr_tool = RemoteToolkit.from_aistudio("asr").get_tools()[0]
ocr_tool = RemoteToolkit.from_aistudio("highacc-ocr").get_tools()[0]

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
async def trans_async(to,query):
    result = await trans_tool(to=to,q=query)
    return result
async def asr_async(dataBase64, format):
    import base64
    file_manager = GlobalFileManagerHandler().get()
    local_file = await file_manager.create_file_from_bytes(file_contents=base64.b64decode(dataBase64), filename="temp")
    return await asr_tool(format=format, speech=local_file.id)
async def ocr_async(dataBase64):
    import base64
    file_manager = GlobalFileManagerHandler().get()
    local_file = await file_manager.create_file_from_bytes(file_contents=base64.b64decode(dataBase64), filename="temp")
    return await ocr_tool(image=local_file.id)

@ocr_asr_bp.route('/translate', methods=["GET", "POST"])
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

@ocr_asr_bp.route('/asr', methods=["GET", "POST"])
def asr():
    dataUrl = request.form.get("dataurl")
    header, dataBase64 = dataUrl.split(";base64,", 1)
    if header == "data:audio/vnd.wave":
        format = "wav"
    elif header == "data:audio/wav":
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

@ocr_asr_bp.route('/ocr', methods=["GET", "POST"])
def ocr():
    dataUrl = request.form.get("dataurl")
    header, dataBase64 = dataUrl.split(";base64,", 1)
    tempMap = run_async(ocr_async,dataBase64)
    resultMap = {'string':'\n'.join(tempMap['words_result'])}
    return jsonify(resultMap)

@ocr_asr_bp.route('/formula', methods=["GET", "POST"])
def dataUrl2Formula():
    # TO DO
    tempMap = {'string':"暂不支持"}
    return jsonify(tempMap)