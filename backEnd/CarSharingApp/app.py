from flask import Flask, session, request, jsonify
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db, cors
from flask_migrate import Migrate
from models import User
import pandas as pd
import config
import re, numpy as np
import pytz
import math



app = Flask(__name__)

#绑定配置文件
app.config.from_object(config)
#数据库初始化
db.init_app(app)
Migrate = Migrate(app,db)
#跨域请求伪造
cors.init_app(app, supports_credentials=True)


#后端接口示例
#用户登录
@app.route('/login', methods=['POST'])
def UserLogin():
    json = request.get_json()
    user = User.query.filter_by(username = json['user_id']).first()
    if user == None:
       return jsonify({'error': '用户不存在！'}), 403
    if check_password_hash(user.password, json['password']):
       session['user_id'] = user.user_id
       return jsonify(session['user_id']), 200
    else:
        return jsonify({'error': '密码错误！'}), 403


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
