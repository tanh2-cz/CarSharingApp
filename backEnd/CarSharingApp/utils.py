# utils.py
import config
from alipay import AliPay, DCAliPay, ISVAliPay
from alipay.utils import AliPayConfig
import uuid
from datetime import datetime


# 生成支付alipay对象，以供调用
def create_alipay():
    alipay = AliPay(
        appid=config.ALIPAY_SETTING.get('ALIPAY_APP_ID'),
        app_notify_url=None,  # 默认回调 url
        app_private_key_string=open(config.ALIPAY_SETTING.get('APP_PRIVATE_KEY_STRING')).read(),
        # 支付宝的公钥，验证支付宝回传消息使用，不是自己的公钥,
        alipay_public_key_string=open(config.ALIPAY_SETTING.get('ALIPAY_PUBLIC_KEY_STRING')).read(),
        sign_type=config.ALIPAY_SETTING.get('SIGN_TYPE'),  # RSA 或者 RSA2
        debug=config.ALIPAY_SETTING.get('ALIPAY_DEBUG'),  # 默认 False
        verbose=False,  # 输出调试数据
        # config=AliPayConfig(timeout=50)  # 可选，请求超时时间
    )
    return alipay

# 生成唯一订单号
def generate_order_number():
    # 获取当前时间并转换为指定格式的字符串
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    # 生成 UUID 并转换为字符串
    unique_id = str(uuid.uuid4().hex)
    # 拼接时间字符串和 UUID 生成订单号
    order_number = f"{current_time}{unique_id}"
    return order_number

