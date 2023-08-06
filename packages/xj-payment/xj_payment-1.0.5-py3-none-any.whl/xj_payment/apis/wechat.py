import json
import logging
import os
from random import sample
from string import ascii_letters, digits


from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from rest_framework.views import APIView
from wechatpayv3 import SignType, WeChatPay, WeChatPayType

# 微信支付商户号（直连模式）或服务商商户号（服务商模式，即sp_mchid)
MCHID = '1627522172'

# 商户证书私钥
# with open('path_to_key/apiclient_key.pem') as f:
#     PRIVATE_KEY = f.read()

# 商户证书序列号
CERT_SERIAL_NO = '444F4864EA9B34415...'

# API v3密钥， https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay3_2.shtml
APIV3_KEY = 'MIIEvQIBADANBgkqhkiG9w0BAQEFAASC...'

# APPID，应用ID或服务商模式下的sp_appid
APPID = 'wx18fd80a15141e4fbo'

# 回调地址，也可以在调用接口的时候覆盖
NOTIFY_URL = 'https://www.xxxx.com/notify'

# 微信支付平台证书缓存目录，减少证书下载调用次数
# 初始调试时可不设置，调试通过后再设置，示例值:'./cert'
CERT_DIR = None

# 日志记录器，记录web请求和回调细节
logging.basicConfig(filename=os.path.join(os.getcwd(), 'demo.log'), level=logging.DEBUG, filemode='a', format='%(asctime)s - %(process)s - %(levelname)s: %(message)s')
LOGGER = logging.getLogger("demo")

# 接入模式:False=直连商户模式，True=服务商模式
PARTNER_MODE = False

# 代理设置，None或者{"https": "http://10.10.1.10:1080"}，详细格式参见https://docs.python-requests.org/zh_CN/latest/user/advanced.html
PROXY = None

class WeChatPayment(APIView):
    def pay(self):
        # 以native下单为例，下单成功后即可获取到'code_url'，将'code_url'转换为二维码，并用微信扫码即可进行支付测试
        wxpay = WeChatPay(
            wechatpay_type=WeChatPayType.NATIVE,
            mchid=MCHID,
            private_key=PRIVATE_KEY,
            cert_serial_no=CERT_SERIAL_NO,
            apiv3_key=APIV3_KEY,
            appid=APPID,
            notify_url=NOTIFY_URL,
            cert_dir=CERT_DIR,
            logger=LOGGER,
            partner_mode=PARTNER_MODE,
            proxy=PROXY)
        out_trade_no = ''.join(sample(ascii_letters + digits, 8))
        description = 'demo-description'
        amount = 1
        code, message = wxpay.pay(
            description=description,
            out_trade_no=out_trade_no,
            amount={'total': amount}
        )
        return JsonResponse({'code': code, 'message': message})
