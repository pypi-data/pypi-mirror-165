from rest_framework.response import Response
from rest_framework.views import APIView

from ..utils.model_handle import parse_data
from ..utils.custom_response import util_response
from ..services.payment_alipay_service import PaymentAlipayService


class PaymentAlipay(APIView):
    def get_pay_url(self, request):
        if self.method == "POST":
            params = parse_data(request)
            data, err_txt = PaymentAlipayService.get_pay_url(params, request)
            if not data:
                return util_response(err=47767, msg=err_txt)
            return Response({
                'err': 0,
                'msg': 'OK',
                'data': data
            })

    def pay_result(self):
        data = self.GET.dict()
