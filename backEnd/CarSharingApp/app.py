from flask import Flask, session, request, jsonify, render_template
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db
from flask_migrate import Migrate # 迁移 确保热更新 而不需要手动删除数据库
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import class_mapper, joinedload
from models import User, ChatGroup, GroupMember, ChatMessage, Wallet, Transaction, Order, GroupNotification
import pandas as pd
import config
import re, numpy as np
import pytz
import math


app = Flask(__name__)

app.config.from_object(config)#绑定配置文件
db.init_app(app)#数据库初始化
migrate = Migrate(app,db)

# cors.init_app(app, resources={r"/*": {"origins": "http://192.168.3.55:8080"}}, supports_credentials=True)#跨域请求伪造

from flask_cors import CORS
CORS(app) # 跨域请求伪造

# 根路由
@app.route('/')
def index():
    return render_template('index.html')

# 统一响应封装
def success(data=None, msg="操作成功"):
    """成功响应"""
    return jsonify({
        "code": 200,
        "msg": msg,
        "data": data or {}
    }), 200

def error(code, msg, http_status=400):
    """错误响应"""
    return jsonify({
        "code": code,
        "msg": msg,
        "data": None
    }), http_status

"""
以下为数据表统一增删改查
"""

################### 辅助函数 ###################

# 序列化结果
# 序列化记录为字典
def serialize_record(record):
    if record is None:
        return None
    # 确保 record 是一个有效的 SQLAlchemy 模型实例
    if not hasattr(record, '__class__') or not hasattr(record.__class__, '__mapper__'):
        # 如果不是模型实例，可能直接返回或抛出错误，这里选择返回 None 或尝试转换为字典
        if isinstance(record, dict):
            return record
        return None # 或者根据需要处理

    mapper = class_mapper(record.__class__)
    columns = [column.key for column in mapper.columns]
    serialized_data = {}
    for column in columns:
        value = getattr(record, column)
        # 特殊处理 datetime 对象，转换为 ISO 格式字符串
        if isinstance(value, datetime):
            # 确保 datetime 对象是 naive 还是 aware (是否包含时区信息)
            if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
                # 如果是 naive datetime (无时区信息)，可以假定为 UTC 或本地时区，或转换为 UTC
                # 这里简单地转换为 ISO 格式，前端可能需要处理时区
                value = value.isoformat()
            else:
                # 确保使用 pytz 处理时区转换
                value = value.astimezone(pytz.utc).isoformat() # 转换为 UTC 并格式化
        serialized_data[column] = value
    return serialized_data

# 辅助函数：检查用户是否为群组成员
def check_group_membership(user_id, group_id):
    """检查用户是否是指定群组的成员"""
    return GroupMember.query.filter_by(user_id=user_id, group_id=group_id).first() is not None
################## 辅助函数 ######################
# 动态获取表模型
def get_model_by_tablename(tablename):
    for model in [User, ChatGroup, GroupMember, ChatMessage, Wallet, Transaction, Order]:
        if model.__tablename__ == tablename:
            return model
    raise ValueError(f"Table '{tablename}' not found.")

# --- 通用 CRUD 接口 ---
# 这几个最简单接口其实是给后端页面用的
@app.route('/add', methods=['POST'])
def add_record():
    data = request.get_json()
    if not data: 
        return error(code=400, msg='请求体必须是JSON格式。')
    
    table_name = data.get('table_name')  # 获取表名
    record_data = data.get('record_data')  # 获取需要插入的数据
    print(record_data)
    print(type(record_data))
    if not table_name or not record_data:
        return error(msg='缺少 table_name 或 record_data。', code=400) # 保持和您之前一致的 code 和 http_status

    try:
        model = get_model_by_tablename(table_name)
        
        # 对密码等敏感字段进行特殊处理
        if table_name == 'users' and 'password_login' in record_data:
            if record_data['password_login']:
                 record_data['password_login'] = generate_password_hash(record_data['password_login'])
            else:
                return error(code=400, msg='新用户密码不能为空。')

        new_record = model(**record_data) # 使用解包操作符将字典数据传递给模型类的构造函数，创建新记录对象
        print(type(new_record))
        db.session.add(new_record)
        db.session.commit()
        print('herae')
        # 动态获取主键值
        # 假设每个表只有一个主键列
        primary_key_name = model.__mapper__.primary_key[0].name
        record_id_value = getattr(new_record, primary_key_name)
        
        # 返回成功消息和记录的主键 ID
        return success(data={'record_id': record_id_value}, msg='记录添加成功！') # 使用应用定义的 success 函数
    
    except ValueError as e: # 通常由 get_model_by_tablename 抛出
        return error(msg=str(e), code=400) # 保持和您之前一致的 code 和 http_status
    except SQLAlchemyError as e:
        db.session.rollback() # 如果发生数据库错误，回滚事务
        app.logger.error(f"添加记录时数据库错误: {str(e)}")
        return error(msg='数据库错误，详情: ' + str(e), code=500, http_status=500) # 保持和您之前一致的 code 和 http_status
    except Exception as e: # 捕获其他潜在错误
        db.session.rollback()
        app.logger.error(f"添加记录时发生意外错误: {str(e)}")
        return error(msg=f'发生意外错误: {str(e)}', code=500, http_status=500)

# 删除记录接口
@app.route('/delete', methods=['DELETE'])
def delete_record():
    data = request.get_json()
    table_name = data.get('table_name')  # 获取表名
    record_id = data.get('record_id')  # 获取记录的主键 ID

    if not table_name or not record_id:
        return error(msg='Missing table_name or record_id', code=403, http_status=400)

    try:
        model = get_model_by_tablename(table_name)
        record = model.query.get(record_id)

        if not record:
            return error(msg=f'Record with id {record_id} not found in table {table_name}', code=403, http_status=404)

        db.session.delete(record)
        db.session.commit()
        return success(data={}, msg='Record deleted successfully')
    except ValueError as e:
        return error(msg=('error: ' + str(e)), code=403, http_status=400)
    except SQLAlchemyError as e:
        # 如果发生数据库错误，回滚事务
        db.session.rollback()
        return error(msg=('Database error, details: ' + str(e)), code=403, http_status=500)

# 修改记录接口
@app.route('/update', methods=['PUT'])
def update_record():
    data = request.get_json()
    table_name = data.get('table_name')  # 获取表名
    record_id = data.get('record_id')  # 获取记录的主键 ID
    field = data.get('field')  # 获取需要修改的字段名
    value = data.get('value')  # 获取字段的新值
    
    if not table_name or not record_id or not field or value is None:
        return error(msg='Missing table_name or record_id', code=403, http_status=400)

    try:
        model = get_model_by_tablename(table_name)
        record = model.query.get(record_id)

        if not record:
            return error(msg=f'Record with id {record_id} not found in table {table_name}', code=403, http_status=404)
        # 检查字段是否存在
        if not hasattr(record, field):
            return error(msg=f'Field "{field}" does not exist in table {table_name}', code=403, http_status=400)

        setattr(record, field, value)# 更新字段值
        db.session.commit()
        return success(data={}, msg='Record updated successfully')
    except ValueError as e:
        return error(msg=f'error: "{str(e)}"', code=403, http_status=400)
    except SQLAlchemyError as e:
        # 如果发生数据库错误，回滚事务
        db.session.rollback()
        return error(msg=f'Database error, detail: "{str(e)}"', code=403, http_status=500)

# 查询记录接口 (已重写并加入分页功能)
@app.route('/query', methods=['GET'])
def query_records():
    table_name = request.args.get('table_name')  # 获取表名
    record_id = request.args.get('record_id')    # 获取记录的主键 ID（可选）
    
    # 保留您添加的打印语句，用于调试
    app.logger.debug(f"接收到查询请求: table_name='{table_name}', record_id='{record_id}'")

    if not table_name:
        # 使用应用定义的 error 函数
        return error(code=400, msg='必须提供 table_name 参数。') # 之前的 code 是 403，通常 400 表示客户端请求错误

    try:
        model = get_model_by_tablename(table_name)

        if record_id:
            # 如果提供了 record_id，则查询单条记录
            app.logger.info(f"查询表 '{table_name}' 中 ID 为 '{record_id}' 的单条记录。")
            record = model.query.get(record_id)
            if not record:
                # 使用应用定义的 error 函数
                return error(code=404, msg=f'在表 {table_name} 中未找到ID为 {record_id} 的记录。', http_status=404)
            # 使用应用定义的 success 函数
            return success(data={'result': serialize_record(record)}, msg="成功获取单条记录。")
        else:
            # 如果未提供 record_id，则查询所有记录并进行分页
            app.logger.info(f"查询表 '{table_name}' 的记录列表（支持分页）。")
            
            # --- 分页参数处理 ---
            try:
                page = int(request.args.get('page', 1))
                # 确保与前端HTML/JS中的itemsPerPage保持一致或允许前端覆盖
                per_page = int(request.args.get('per_page', 10)) # 假设前端默认每页10条
                if page < 1: page = 1
                if per_page < 1: per_page = 1
                if per_page > 100: per_page = 100 # 防止一次请求过多数据
            except ValueError:
                return error(code=400, msg="分页参数 'page' 和 'per_page' 必须是有效的整数。")
            
            app.logger.debug(f"请求页码: {page}, 每页数量: {per_page}")

            # --- 动态过滤条件构建 (可选，当前版本未实现此部分的复杂过滤，仅基础查询) ---
            # 如果需要基于其他URL参数进行过滤，可以在这里添加逻辑
            # query_filters = {}
            # for key, value in request.args.items():
            #     if key not in ['table_name', 'record_id', 'page', 'per_page'] and hasattr(model, key):
            #         query_filters[key] = value
            # base_query = model.query.filter_by(**query_filters)
            
            base_query = model.query # 基础查询，后续可以添加 .filter_by() 或 .filter()
            
            # --- 排序逻辑 ---
            # 默认按主键降序排列，以确保分页结果的一致性
            try:
                pk_column_name = model.__mapper__.primary_key[0].name
                pk_column = getattr(model, pk_column_name)
                ordered_query = base_query.order_by(pk_column.desc())
                app.logger.debug(f"按主键 '{pk_column_name}' 降序排序。")
            except (AttributeError, IndexError):
                app.logger.warning(f"无法确定表 '{table_name}' 的主键进行排序，将使用数据库默认排序。")
                ordered_query = base_query # 无特定排序

            # --- 执行分页查询 ---
            pagination_obj = ordered_query.paginate(page=page, per_page=per_page, error_out=False)
            results = pagination_obj.items
            
            serialized_results = [serialize_record(record) for record in results]
            
            response_data = {
                'items': serialized_results,
                'total': pagination_obj.total,
                'page': pagination_obj.page,
                'per_page': pagination_obj.per_page,
                'pages': pagination_obj.pages
            }
            # 使用应用定义的 success 函数
            return success(data=response_data, msg=f"成功获取表 '{table_name}' 的记录列表。")
        
    except ValueError as e: # 通常由 get_model_by_tablename 抛出
        app.logger.error(f"值错误: {str(e)}")
        # 使用应用定义的 error 函数
        return error(code=400, msg=str(e))
    except SQLAlchemyError as e:
        app.logger.error(f"查询记录时数据库错误: {str(e)}")
        db.session.rollback() # 确保回滚
        # 使用应用定义的 error 函数
        return error(code=500, msg='数据库查询时发生错误。详情: ' + str(e), http_status=500)
    except Exception as e:
        app.logger.error(f"查询记录时发生未知错误: {str(e)}")
        # 使用应用定义的 error 函数
        return error(code=500, msg='处理查询时发生未知错误。', http_status=500)

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
    required_fields = ['username', 'phone', 'password']
    for field in required_fields:
        if field not in data or not data[field]:
            return error(code=403, msg=f'{field} 不能为空！') # 统一 403 一刀切处理

    username = data['username']
    phone_number = data['phone']
    password_login = data['password']

    if User.query.filter_by(username=username).first():
        return error(code=403, msg='该用户名已被使用！')

    if User.query.filter_by(phone_number=phone_number).first():
        return error(code=403, msg='手机号已被注册！')

    hashed_password = generate_password_hash(password_login)# 生成密码哈希值

    new_user = User(
        username=username,
        nickname=username,
        phone_number=phone_number,
        password_login=hashed_password,
        role='乘客'  # 默认角色为乘客
    )

    db.session.add(new_user)
    db.session.commit()
    return success(msg='注册成功！')


# 用户登录接口
@app.route('/login', methods=['POST'])
def user_login():
    data = request.get_json()

    # 检查必填字段是否完整
    required_fields = ['username', 'password']
    for field in required_fields:
        if field not in data or not data[field]:
            # TODO: 状态码用全局参数
            return error(msg=f'{field} 不能为空！', code=400)

    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if not user:
        return error(msg='用户不存在！', code=403)

    if not check_password_hash(user.password_login, password):
        return error(msg='密码错误！', code=403)

    session['user_id'] = user.user_id    # 将用户 ID 存入 session

    return success(data={'user_id': user.user_id}, msg=f'用户{user.user_id}已登录!')    # 返回用户 ID


# 用户登出接口
@app.route('/logout', methods=['POST'])
def user_logout():
    # TODO: 多个用户怎么办？
    session.pop('user_id', None)  # 清除 session 中的 user_id
    return success(msg='登出成功！')

# 查询所有的通知 过滤交给前端了
# 获取所有群聊通知接口
# 返回拼车群通知、有通知的群聊的详细信息 join 后的结果
# @app.route('/query/group_notify', methods=['GET'])
# def query_group_notify():
#     # data = request.get_json()

#     # 有个问题 如果用户把某个通知删了 他刷新了再调用这个接口还会获得列表
#     # 算了那就只让用户过滤不让用户删除
#     # TODO: 后面如果用户多了应该是要用 cookie 机制的
#     if 'user_id' not in session:
#         # TODO: 加游客访问功能
#         return error(code=401, msg='用户未登录或会话已过期，请先登录！', http_status=401)
    
#     group_notifys = db.session.query(GroupNotification).join(
#         ChatGroup, ChatGroup.group_id == GroupNotification.group_id
#     )

#     group_notifys = [serialize_record(group_notify) for group_notify in group_notifys]
#     return success(data={'notifications': group_notifys}, msg='成功获取到群聊通知列表')

# 群通知的分页查询
# --- 群通知接口 (沿用之前的逻辑，稍作调整) ---
@app.route('/query/group_notify', methods=['GET'])
def query_group_notify():
    if 'user_id' not in session:
        return error(code=401, msg='用户未登录或会话已过期，请先登录！', http_status=401)
    
    current_user_id = session['user_id']
    app.logger.info(f"用户 {current_user_id} 正在查询群通知。")

    try:
        all_notifications_query = GroupNotification.query.order_by(GroupNotification.created_at.desc())
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        # 分页
        pagination = all_notifications_query.paginate(page=page, per_page=per_page, error_out=False)
        all_notifications = pagination.items
        notifications_data = []
        for notification_item in all_notifications:
            serialized_notification = serialize_record(notification_item)
            # 一个正确的消息肯定是有 group 字段的
            if notification_item.group:
                # 把消息对应的 group 详情变成 键-值
                serialized_notification['group_details'] = serialize_record(notification_item.group)
            else:
                serialized_notification['group_details'] = None
            notifications_data.append(serialized_notification)
        if not all_notifications and page == 1:
             # 什么结果都没有查到
             return success(data={'items': [], 'total': 0, 'page': 1, 'per_page': per_page, 'pages': 0}, msg="当前没有群聊通知。")
        return success(data={'items': notifications_data, 'total': pagination.total, 'page': pagination.page, 'per_page': pagination.per_page, 'pages': pagination.pages}, msg='成功获取到群聊通知列表')
    except SQLAlchemyError as e:
        db.session.rollback(); app.logger.error(f"查询加群通知时数据库错误: {str(e)}")
        return error(code=500, msg='数据库查询加群通知失败。', http_status=500)
    except Exception as e:
        app.logger.error(f"查询加群通知时发生意外错误: {str(e)}")
        return error(code=500, msg='获取加群通知时发生未知错误。', http_status=500)

# 返回用户加入的群聊和用户创建的群聊
# 群聊的用户同步
# @app.route('/query/user_groups', methods=['GET'])
# def query_user_groups():
#     # data = request.get_json()

#     # 有个问题 如果用户把某个通知删了 他刷新了再调用这个接口还会获得列表
#     # 算了那就只让用户过滤不让用户删除
#     if 'user_id' not in session:
#         # TODO: 加游客访问功能 游客模式也算一个亮点吧
#         return error(code=401, msg='用户未登录或会话已过期，请先登录！', http_status=401)
    
#     group_my_create = db.session.query(ChatGroup).join(
#         ChatGroup, ChatGroup.group_id == GroupNotification.group_id
#     )

#     group_my_join = 

#     group_notifys = [serialize_record(group_notify) for group_notify in group_notifys]
#     return success(data={'my_create': group_notifys, 'my_join': group_notifys}, msg='成功获取到"我的群聊"列表')

# 获取我加入的群聊和我创建的群聊
# --- 群聊相关接口 ---
@app.route('/get/user_groups', methods=['GET'])
def query_user_groups_distinguished(): # 重命名函数以区分

    if 'user_id' not in session:
        return error(code=401, msg='用户未登录或会话已过期，请先登录！', http_status=401)
    
    current_user_id = session['user_id'] # TODO: 要不要传 user id 过来 ?
    app.logger.info(f"用户 {current_user_id} 正在查询其创建的和加入的群聊列表。")

    try:
        # 1. 查询用户创建的群聊
        created_groups_query = ChatGroup.query.join(
            Order, ChatGroup.order_id == Order.order_id
        ).filter(
            Order.user_id == current_user_id
        ).options(
            joinedload(ChatGroup.members) # 预加载成员以计算数量
        )
        created_groups_list = created_groups_query.all()
        
        created_groups_data = []
        created_group_ids = set() # 用于后续排除
        for group in created_groups_list:
            serialized_group = serialize_record(group)
            serialized_group['member_count'] = len(group.members) if group.members else 0
            serialized_group['is_creator'] = True # 明确标记为创建者
            created_groups_data.append(serialized_group)
            created_group_ids.add(group.group_id)

        # 2. 查询用户加入但非创建的群聊
        # 首先获取用户是成员的所有群聊
        all_member_groups_query = ChatGroup.query.join(
            GroupMember, ChatGroup.group_id == GroupMember.group_id
        ).filter(
            GroupMember.user_id == current_user_id
        ).options(
            joinedload(ChatGroup.members) # 预加载成员以计算数量
        )
        all_member_groups_list = all_member_groups_query.all()

        joined_only_groups_data = []
        for group in all_member_groups_list:
            if group.group_id not in created_group_ids: # 排除已在创建列表中的群聊
                serialized_group = serialize_record(group)
                serialized_group['member_count'] = len(group.members) if group.members else 0
                serialized_group['is_creator'] = False # 明确标记为非创建者 (因为已排除)
                joined_only_groups_data.append(serialized_group)
        
        return success(data={
            'created_groups': created_groups_data,
            'joined_groups': joined_only_groups_data # 此处为仅加入未创建的群聊
        }, msg='成功获取到您创建的和加入的群聊列表')

    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"为用户 {current_user_id} 查询创建/加入群组时数据库错误: {str(e)}")
        return error(code=500, msg='数据库查询群聊列表失败，请稍后重试。', http_status=500)
    except Exception as e:
        app.logger.error(f"为用户 {current_user_id} 查询创建/加入群组时发生意外错误: {str(e)}")
        return error(code=500, msg='获取群聊列表时发生未知错误。', http_status=500)
    
# 单个群聊的聊天记录
@app.route('/get/group/<int:group_id>/messages', methods=['GET'])
def get_group_messages(group_id):
    if 'user_id' not in session:
        return error(code=401, msg='用户未登录或会话已过期！', http_status=401)
    current_user_id = session['user_id'] # TODO: 这不又要面对多用户问题 ?

    if not check_group_membership(current_user_id, group_id):
        return error(code=403, msg='您不是该群组成员，无权查看消息。', http_status=403)

    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int) # 前端通常一次加载20-50条

        # 按发送时间升序排列，方便前端实现“上拉加载更早消息”
        # joinedload 是 SQLAlchemy ORM (对象关系映射器) 中的一个查询选项 (Query Option)，
        # 用于优化关联对象的加载。它的主要目的是解决或避免 N+1 查询问题，从而提高数据库查询效率。
        # 
        # 当您查询一个主对象（例如 ChatGroup），并且您知道您很快会需要访问与它关联的对象
        # （例如 ChatGroup.members 或 ChatMessage.user）时，joinedload 会告诉 SQLAlchemy 
        # 在同一次数据库查询中，通过 SQL 的 JOIN 操作，将主对象和其指定的关联对象一起加载出来。
        messages_query = ChatMessage.query.filter_by(group_id=group_id)\
            .options(joinedload(ChatMessage.user))\
            .order_by(ChatMessage.sent_at.asc()) # 或者 .desc() 取决于前端如何展示
        
        pagination = messages_query.paginate(page=page, per_page=per_page, error_out=False)
        messages = pagination.items
        
        messages_data = []
        for msg in messages:
            sender_info = {}
            if msg.user: # 确保关联的 user 对象存在
                # TODO: 我觉得要做个个人主页啊 点进一个人的头像进去就是个人主页
                sender_info = {
                    'user_id': msg.user.user_id,
                    'nickname': msg.user.nickname,
                    'avatar': msg.user.avatar
                }
            # TODO: 删除消息接口
            messages_data.append({
                'message_id': msg.message_id,
                'group_id': msg.group_id,
                'message_text': msg.message_text,
                'sent_at': msg.sent_at.isoformat() if msg.sent_at else None,
                'sender': sender_info
            })
        
        return success(data={
            'items': messages_data,
            'total': pagination.total,
            'page': pagination.page,
            'per_page': pagination.per_page,
            'pages': pagination.pages
        }, msg='成功获取群聊消息。')
    except SQLAlchemyError as e:
        app.logger.error(f"获取群聊 {group_id} 消息时数据库错误: {str(e)}")
        return error(code=500, msg='数据库查询群消息失败。', http_status=500)
    except Exception as e:
        app.logger.error(f"获取群聊 {group_id} 消息时发生意外错误: {str(e)}")
        return error(code=500, msg='获取群消息时发生未知错误。', http_status=500)

if __name__ == '__main__':
    with app.app_context():
        # 后端启动时创建所有表
        db.create_all()
    app.run(host='0.0.0.0', port=config.BACKEND_PORT, debug=True)
