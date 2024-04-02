# from collect.models import Collect
# from payment.models import Payment
#
#
# def add_and_save_amount_now(
#         collect: Collect,
#         payment: Payment
# ) -> int:
#     """
#     Функция для добавления значение для M2M Collect.donates
#     @param collect: объект на который ссылается платеж
#     @param payment: объект самого платежа
#     """
#     collect.amount_now += payment.amount
#     collect.save()
#     collect.refresh_from_db()
#     return collect.amount_now
