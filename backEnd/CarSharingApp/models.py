from exts import db
from datetime import datetime

# 用户表 (users)
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)  # 用户名
    nickname = db.Column(db.String(50), nullable=False) # 昵称
    avatar = db.Column(db.String(255)) # 头像
    level = db.Column(db.Integer, default=1) # 用户等级
    role = db.Column(db.String(20), nullable=False)  # 司机/乘客
    credit_score = db.Column(db.Integer, default=100) # 信用分
    total_distance = db.Column(db.Float, default=0.0) # 总行驶里程
    carpool_count = db.Column(db.Integer, default=0) # 拼车次数
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password_login = db.Column(db.String(255), nullable=False)
    password_pay = db.Column(db.String(255))
    verified = db.Column(db.Boolean, default=False)

    # 关联关系
    orders = db.relationship('Order', backref='user', lazy=True)
    wallet = db.relationship('Wallet', backref='user', uselist=False, lazy=True)
    group_members = db.relationship('GroupMember', backref='user', lazy=True)
    messages = db.relationship('ChatMessage', backref='user', lazy=True)

class Notification(db.Model):

    __tablename__ = 'notifications'

    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 群聊表 (chat_groups)
class ChatGroup(db.Model):
    __tablename__ = 'chat_groups'

    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    group_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关联关系
    members = db.relationship('GroupMember', backref='group', lazy=True)
    messages = db.relationship('ChatMessage', backref='group', lazy=True)


# 群聊成员表 (group_members)
class GroupMember(db.Model):
    __tablename__ = 'group_members'

    member_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer, db.ForeignKey('chat_groups.group_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(20), nullable=False)  # 乘客/司机


# 聊天记录表 (chat_messages)
class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'

    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer, db.ForeignKey('chat_groups.group_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    message_text = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)


# 支付与钱包表 (wallets)
class Wallet(db.Model):
    __tablename__ = 'wallets'

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    balance = db.Column(db.Float, default=0.0)  # 账户余额
    # 微信支付相关字段
    wechat_account = db.Column(db.String(100), unique=True, nullable=True)  # 微信账号
    is_wechat_bound = db.Column(db.Boolean, default=False)  # 是否绑定了微信支付
    # 支付宝支付相关字段
    alipay_account = db.Column(db.String(100), unique=True, nullable=True)  # 支付宝账号
    is_alipay_bound = db.Column(db.Boolean, default=False)  # 是否绑定了支付宝支付

    # 关联关系
    # user = db.relationship('User', backref='wallet', uselist=False, lazy=True)


# 支付交易记录表 (transactions)
class Transaction(db.Model):
    __tablename__ = 'transactions'

    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 充值/支付
    amount = db.Column(db.Float, nullable=False)
    transaction_time = db.Column(db.DateTime, default=datetime.utcnow)


# 订单表 (orders)
class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    start_location = db.Column(db.String(255), nullable=False)
    end_location = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 匹配中/进行中/已完成
    fare = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关联关系
    chat_group = db.relationship('ChatGroup', backref='order', uselist=False, lazy=True)