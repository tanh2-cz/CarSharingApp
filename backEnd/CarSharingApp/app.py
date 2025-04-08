from flask import Flask, session, request, jsonify
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db, cors
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import class_mapper
from models import User, ChatGroup, GroupMember, ChatMessage, Wallet, Transaction, Order
import pandas as pd
import config
import re, numpy as np
import pytz
import math


app = Flask(__name__)

app.config.from_object(config)#绑定配置文件
db.init_app(app)#数据库初始化
Migrate = Migrate(app,db)
cors.init_app(app, supports_credentials=True)#跨域请求伪造


"""
以下为数据表统一增删改查
"""

# 动态获取表模型
def get_model_by_tablename(tablename):
    for model in [User, ChatGroup, GroupMember, ChatMessage, Wallet, Transaction, Order]:
        if model.__tablename__ == tablename:
            return model
    raise ValueError(f"Table '{tablename}' not found.")

# 增加记录接口
@app.route('/add', methods=['POST'])
def add_record():
    data = request.get_json()
    table_name = data.get('table_name')  # 获取表名
    record_data = data.get('record_data')  # 获取需要插入的数据

    if not table_name or not record_data:
        return jsonify({'error': 'Missing table_name or record_data'}), 400

    try:
        model = get_model_by_tablename(table_name)
        new_record = model(**record_data)# 使用解包操作符将字典数据传递给模型类的构造函数，创建新记录对象
        db.session.add(new_record)
        db.session.commit()
        # 返回成功消息和记录的主键 ID
        return jsonify({'message': 'Record added successfully', 'record_id': new_record.id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except SQLAlchemyError as e:
        # 如果发生数据库错误，回滚事务
        db.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500

# 删除记录接口
@app.route('/delete', methods=['DELETE'])
def delete_record():
    data = request.get_json()
    table_name = data.get('table_name')  # 获取表名
    record_id = data.get('record_id')  # 获取记录的主键 ID

    if not table_name or not record_id:
        return jsonify({'error': 'Missing table_name or record_id'}), 400

    try:
        model = get_model_by_tablename(table_name)
        record = model.query.get(record_id)

        if not record:
            return jsonify({'error': f'Record with id {record_id} not found in table {table_name}'}), 404

        db.session.delete(record)
        db.session.commit()
        return jsonify({'message': 'Record deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except SQLAlchemyError as e:
        # 如果发生数据库错误，回滚事务
        db.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500

# 修改记录接口
@app.route('/update', methods=['PUT'])
def update_record():
    data = request.get_json()
    table_name = data.get('table_name')  # 获取表名
    record_id = data.get('record_id')  # 获取记录的主键 ID
    field = data.get('field')  # 获取需要修改的字段名
    value = data.get('value')  # 获取字段的新值

    if not table_name or not record_id or not field or value is None:
        return jsonify({'error': 'Missing table_name, record_id, field, or value'}), 400

    try:
        model = get_model_by_tablename(table_name)
        record = model.query.get(record_id)

        if not record:
            return jsonify({'error': f'Record with id {record_id} not found in table {table_name}'}), 404
        # 检查字段是否存在
        if not hasattr(record, field):
            return jsonify({'error': f'Field "{field}" does not exist in table {table_name}'}), 400

        setattr(record, field, value)# 更新字段值
        db.session.commit()
        return jsonify({'message': 'Record updated successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except SQLAlchemyError as e:
        # 如果发生数据库错误，回滚事务
        db.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500

# 查询记录接口
@app.route('/query', methods=['GET'])
def query_records():
    table_name = request.args.get('table_name')  # 获取表名
    record_id = request.args.get('record_id')  # 获取记录的主键 ID（可选）

    if not table_name:
        return jsonify({'error': 'Missing table_name'}), 400

    try:
        model = get_model_by_tablename(table_name)

        if record_id:
            # 如果提供了 record_id，则查询单条记录
            record = model.query.get(record_id)
            if not record:
                return jsonify({'error': f'Record with id {record_id} not found in table {table_name}'}), 404
            # 序列化记录为字典格式
            return jsonify({'result': serialize_record(record)}), 200
        else:
            # 如果未提供 record_id，则查询所有记录
            results = model.query.all()
            # 序列化所有记录为字典格式
            serialized_results = [serialize_record(record) for record in results]
            return jsonify({'results': serialized_results}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except SQLAlchemyError as e:
        return jsonify({'error': 'Database error', 'details': str(e)}), 500

# 序列化记录为字典
def serialize_record(record):
    columns = [column.key for column in class_mapper(record.__class__).columns]
    return {column: getattr(record, column) for column in columns}

"""
以下为身份管理
"""
# 用户注册接口
@app.route('/signup', methods=['POST'])
def user_signup():
    data = request.get_json()

    # 检查必填字段是否完整
    required_fields = ['nickname', 'phone_number', 'password_login']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'{field} 不能为空！'}), 400

    nickname = data['nickname']
    phone_number = data['phone_number']
    password_login = data['password_login']

    if User.query.filter_by(nickname=nickname).first():
        return jsonify({'error': '昵称已被使用！'}), 403

    if User.query.filter_by(phone_number=phone_number).first():
        return jsonify({'error': '手机号已被注册！'}), 403


    hashed_password = generate_password_hash(password_login)# 生成密码哈希值

    new_user = User(
        nickname=nickname,
        phone_number=phone_number,
        password_login=hashed_password,
        role='乘客'  # 默认角色为乘客
    )

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': '注册成功！'}), 201


# 用户登录接口
@app.route('/login', methods=['POST'])
def user_login():
    data = request.get_json()

    # 检查必填字段是否完整
    required_fields = ['phone_number', 'password_login']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'{field} 不能为空！'}), 400

    phone_number = data['phone_number']
    password_login = data['password_login']

    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        return jsonify({'error': '用户不存在！'}), 403

    if not check_password_hash(user.password_login, password_login):
        return jsonify({'error': '密码错误！'}), 403

    session['user_id'] = user.user_id    # 将用户 ID 存入 session

    return jsonify({'user_id': user.user_id}), 200    # 返回用户 ID


# 用户登出接口
@app.route('/logout', methods=['POST'])
def user_logout():
    session.pop('user_id', None)  # 清除 session 中的 user_id
    return jsonify({'message': '登出成功！'}), 200


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
