
from flask import Flask, g
from flask_cors import CORS
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resource={r'/*': {'origins': '*'}})

# session密钥
app.secret_key = '07111D358A778EE6CBCE31854F44457A'

# 注册蓝图
from userapi import user_bp
from nlpapi import nlp_bp
from ocr_asrapi import ocr_asr_bp
app.register_blueprint(user_bp)
app.register_blueprint(nlp_bp)
app.register_blueprint(ocr_asr_bp)

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        print("close db")
        db.close()

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)