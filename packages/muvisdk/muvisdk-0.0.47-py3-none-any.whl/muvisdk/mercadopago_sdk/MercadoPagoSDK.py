import mercadopago
from .Customer import Customer
from .Card import Card
from .CardToken import CardToken
from .Payment import Payment
from .Refund import Refund


class MercadoPagoSDK:
    def __init__(self, merchant: dict, marketplace: bool = False):
        active = True
        if 'credentials' in merchant and 'mercadopago' in merchant['credentials'] and not marketplace:
            active = merchant['credentials']['mercadopago']['active']
            access_token = merchant['credentials']['mercadopago']['access_token'] if active else None
        elif 'credentials' in merchant and 'mp_marketplace' in merchant['credentials'] and marketplace:
            active = merchant['credentials']['mp_marketplace']['active']
            access_token = merchant['credentials']['mp_marketplace']['access_token'] if active else None
        else:
            access_token = merchant['keys_marketplace']['access_token'] if marketplace else merchant['keys']['access_token']
        self.sdk = mercadopago.SDK(access_token) if active else None
        self.merchant_id = merchant['_id']
        self.merchant_name = merchant['name']
        self.processor = 'mercadopago'

    def customer(self):
        return Customer(self.processor, self.sdk)
    
    def card(self):
        return Card(self.processor, self.sdk)

    def card_token(self):
        return CardToken(self.processor, self.sdk)
    
    def payment(self):
        return Payment(self.processor, self.sdk, self.merchant_id)

    def refund(self):
        return Refund(self.processor, self.sdk)

    def ok(self):
        return self.sdk is not None
