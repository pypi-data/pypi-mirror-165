import random
from config.config import Config
from ..utils.common import get_domain
from ..utils.alipay_utils import *
from django.utils import timezone

gatway = Config.getIns().get("xj_payment", "GATEWAY", "https://openapi.alipaydev.com/gateway.do")


class PaymentAlipayService:
    @staticmethod
    def get_pay_url(params, host):
        # 生成支付宝支付链接地址
        domain_name = get_domain(host)
        money = params['money']
        out_trade_no = timezone.now().strftime('%Y%m%d%H%M%S') + ''.join(map(str, random.sample(range(0, 9), 6)))
        notify_url = domain_name + '/api/payment/update_order/'
        alipay = my_ali_pay(notify_url)
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=params['out_trade_no'],  # 订单编号
            total_amount=str(money),  # 交易金额(单位: 元 保留俩位小数)   这里一般是从前端传过来的数据
            subject=f"紫薇系统-{params['out_trade_no']}",  # 商品名称或产品名称
            return_url=domain_name + "/api/payment/get_result/",  # 支付成功后跳转的页面，App支付此参数无效，集成支付宝SDK自带跳转
        )
        # 拼接支付链接，注意：App支付不需要返回支付宝网关
        ali_pay_url = order_string if is_app_pay(order_string) else gatway + "?" + order_string
        return ali_pay_url, None
