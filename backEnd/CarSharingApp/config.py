import os

# MySQL所在的主机名
HOSTNAME = "127.0.0.1"
# MySQL监听的端口号，默认3306
PORT = 3306
# 连接MySQL的用户名
USERNAME = "root"
# 连接MySQL的密码
PASSWORD = "20040504"
# MySQL上创建的数据库名称
DATABASE = "CarAppDb"
DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
SQLALCHEMY_DATABASE_URI = DB_URI

BACKEND_PORT = 5555 # 后端端口号 设置成了 5555 防止冲突

# 用于加密 session 的密钥
SECRET_KEY = os.urandom(24)

# 支付宝支付相关配置
BASE_DIR = os.path.dirname(__file__)

ALIPAY_SETTING = {
    'ALIPAY_APP_ID': "2021000148685540",  # APPID(上线之后需要改成，真实应用的appid)
    'APLIPAY_APP_NOTIFY_URL': None,  # 应用回调地址[支付成功以后,支付宝返回结果到哪一个地址下面] 一般这里不写，用下面的回调地址即可
    'ALIPAY_DEBUG': False,
    # APIPAY_GATEWAY="https://openapi.alipay.com/gateway.do"   # 上线后的真实网关
    'APIPAY_GATEWAY': "https://openapi-sandbox.dl.alipaydev.com/gateway.do",  # 沙盒环境的网关(上线需要进行修改)
    'ALIPAY_RETURN_URL': "http://127.0.0.1:5000/alipay/result/",  # 同步回调地址，用于前端,支付成功之后回调
    'ALIPAY_NOTIFY_URL': "http://127.0.0.1:5000/alipay/result/",  # 异步回调网址，后端使用，post请求，网站未上线，post无法接收到响应内容，付成功之后回调
    'APP_PRIVATE_KEY_STRING': os.path.join(BASE_DIR, 'keys/private.key'),  # 自己生成的私钥，这个就是路径拼接
    # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,********
    'ALIPAY_PUBLIC_KEY_STRING': os.path.join(BASE_DIR, 'keys/public.key'),  # 支付宝公钥
    'SIGN_TYPE': "RSA2",  # RSA 或者 RSA2  现在基本上都是用RSA2
}
