import requests
import json

from ..MuviBase import MuviBase


class Refund(MuviBase):
    def __init__(self, processor: str, url: str, private_key: str, public_key: str):
        super().__init__(processor)
        self.url = url
        self.private_key = private_key
        self.public_key = public_key
        self.headers = {
            'apikey': self.private_key,
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache'
        }

    def create(self, processor: str, payment_id: str, amount: float = None) -> dict:
        data = {
            'amount': round(amount, 2) * 100 if amount else amount
        }
        r = requests.post(self.url + f'/payments/{payment_id}/refunds', headers=self.headers, data=json.dumps(data))
        if r.status_code > 400:
            return self.ok(response=r.json(), status=r.status_code)
        return self.error(response=r.json(), status=r.status_code)
