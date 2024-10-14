from flask import Blueprint, request, stream_with_context, Response, jsonify
import openai
from userapi import checkUser

API_KEY = "sk-296ad1237ecd4259bce279b1c549cd88"
client = openai.OpenAI(
    api_key=API_KEY, 
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

nlp_bp = Blueprint('nlp', __name__)

# 用于将openai.Stream转化为文本流生成器
def generate_stream(response_stream : openai.Stream):
    try:
        for chunk in response_stream:
            yield chunk.choices[0].delta.content
    except Exception as e:
        yield "error"

# 文本操作类请求的基本函数
def ask(askCont):
    username= request.form.get("user")
    key = request.form.get("key")
    if not checkUser(username, key):
        return "permission denied"
    try:
        response_stream = client.chat.completions.create(
            model="qwen-turbo",
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': askCont}],
            stream=True,
            )
        return Response(stream_with_context(
            generate_stream(response_stream)
            ))
    except:
        return "error"

# 润色
@nlp_bp.route('/getpolish', methods=["GET", "POST"])
def getpolish():
    quesCont = request.form.get("cont")
    askCont = "帮我润色下面这段话（请直接输出结果，不要在开头和结尾增加额外信息）:" + quesCont
    return ask(askCont)

# 缩写
@nlp_bp.route('/getabbreviate', methods=["GET", "POST"])
def getabbreviate():
    quesCont = request.form.get("cont")
    askCont = "帮我缩写下面这段话（请直接输出结果，不要在开头和结尾增加额外信息）:" + quesCont
    return ask(askCont)

# 扩写
@nlp_bp.route('/getexpand', methods=["GET", "POST"])
def getexpand():
    quesCont = request.form.get("cont")
    askCont = "帮我扩写下面这段话（请直接输出结果，不要在开头和结尾增加额外信息）:" + quesCont
    return ask(askCont)

# 续写
@nlp_bp.route('/getextend', methods=["GET", "POST"])
def getextend():
    quesCont = request.form.get("cont")
    askCont = "帮我续写下面这段话（请直接输出结果，不要在开头和结尾增加额外信息）:" + quesCont
    return ask(askCont)