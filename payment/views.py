from rest_framework.generics import (CreateAPIView,
                                     ListAPIView,
                                     RetrieveAPIView,
                                     UpdateAPIView,
                                     DestroyAPIView)
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated)

from collect.models import Collect
from payment.models import Payment
from payment.serializers import PaymentCreateSerializer


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentCreateSerializer
    permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     super().perform_create(serializer)
    #     recipient = serializer.data['recipient']
    #     collect = Collect.objects.filter(id=recipient)
        # donat = collect.donates.

