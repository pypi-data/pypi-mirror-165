from rest_framework.response import Response

from xj_payment.models import PaymentOrder


class PaymentService:
    def create(self, data):
        print(data)
        payment_order = PaymentOrder.objects.create(**data)
        return Response({
            'err': 0,
            'msg': '',
            'data': {
                "contact_book_id": payment_order.id,
            }})
