from .Customer import Customer
from .Card import Card
from .CardToken import CardToken
from .Payment import Payment
from .Refund import Refund


class DecidirSDK:
    def __init__(self, merchant: dict, merchant_cadena: dict, marketplace: bool = False):
        if 'credentials' not in merchant or 'decidir' not in merchant['credentials'] or not merchant['credentials']['decidir']['active']:
            self.private_key = None
            return
        credentials_cadena = merchant_cadena['credentials']['decidir']
        credentials_local = merchant['credentials']['decidir']
        self.url = 'https://developers.decidir.com/api/v2'
        self.private_key = credentials_cadena['access_token']
        self.public_key = credentials_cadena['public_key']
        self.merchant_name = merchant['name']
        self.site_id = credentials_local['site_id']
        self.site_id_cadena = credentials_cadena['site_id']
        self.processor = 'decidir'
        self.marketplace = marketplace

    def customer(self):
        return Customer(self.processor, self.url, self.private_key, self.public_key)
    
    def card(self):
        return Card(self.processor, self.url, self.private_key, self.public_key)

    def card_token(self):
        return CardToken(self.processor, self.url, self.private_key, self.public_key)

    def payment(self):
        return Payment(self.processor, self.url, self.private_key, self.public_key, self.merchant_name, self.site_id,
                       self.site_id_cadena, self.marketplace)

    def refund(self):
        return Refund(self.processor, self.url, self.private_key, self.public_key)

    def ok(self):
        return self.private_key is not None
