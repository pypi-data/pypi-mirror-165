import requests
import random
import string
from iso8601 import parse_date
import pytz
from ..MuviBase import MuviBase


arg_tz = pytz.timezone('America/Buenos_Aires')

def _format_card(response):
    if 'card' in response:
        return {
            'id': response['card']['id'],
            'card_type': 'not_found',
            'last_four_digits': response['card']['last_four_digits'],
            'cardholder': {
                'name': response['card']['cardholder']['name']
            },
            'expiration_month': response['card']['expiration_month'],
            'expiration_year': response['card']['expiration_year'],
        }
        
    if 'card_data' in response and 'tokens' not in response['card_data']:
        return {
            'id': '',
            'card_type': '',
            'last_four_digits': response['card_data']['card_number'][-4:],
            'cardholder': {
                'name': response['card_data']['card_holder']['name']
            },
            'expiration_month': '',
            'expiration_year': '',
        }
    
    return {
        'id': '',
        'card_type': '',
        'last_four_digits': '',
        'cardholder': {
            'name': ''
        },
        'expiration_month': '',
        'expiration_year': '',
    }


def _format(response):
    if response['status'] in ['accredited', 'approved']:
        response['status'] = 'approved'
        response['status_detail'] = 'accredited'
    elif response['status'] == 'rejected':
        response['status_detail'] = 'rejected'

    date = parse_date(response['date']).astimezone(arg_tz)
    result = {
        'id': response['site_transaction_id'],
        'payment_id': response['id'],
        'transaction_amount': response['amount'] / 100,
        'date_created': date,
        'status': response['status'],
        'status_detail': response['status_detail'],
        'card': _format_card(response),
        'payment_day': date
    }
    return result


class Payment(MuviBase):
    def __init__(self, processor: str, url: str, private_key: str, public_key: str, merchant_name: str, site_id: str,
                 site_id_cadena: str):
        super().__init__(processor)
        self.url = url
        self.private_key = private_key
        self.public_key = public_key
        self.merchant_name = merchant_name
        self.site_id = site_id
        self.site_id_cadena = site_id_cadena
        self.headers = {
            'apikey': self.private_key,
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache'
        }

    def create(self, payment_data: dict):
        site_transaction_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        total_amount = round(payment_data['transaction_amount'], 2) * 100  # se multiplica por 100; no acepta decimales
        installments = payment_data['installments'] if 'installments' in payment_data else 1
        body = {
            'customer': {
                'id': payment_data['payer']['decidir_id'],
                'email': payment_data['payer']['email']
            },
            'site_id':self.site_id_cadena,
            'site_transaction_id': site_transaction_id,
            'token': payment_data['token'],
            'payment_method_id': 1,         # Peso Argentino
            'bin': payment_data['bin'],     # primeros 6 digitos de la tarjeta
            'currency': 'ARS',
            'payment_type': 'single',
            'establishment_name': self.merchant_name,
            'sub_payments': [],
            'amount':total_amount, # En cualquier tipo de payment
        }

        if 'application_fee' not in payment_data:   # El pago va 100% al hijo
            body['site_id'] = self.site_id
            body['installments'] = installments
        else:
            application_fee = round(payment_data['application_fee'], 2) * 100
            body['payment_type'] = 'distributed'
            body['sub_payments'] = [
                {
                    'site_id': self.site_id_cadena,
                    'installments': installments,
                    'amount': application_fee
                }, {
                    'site_id': self.site_id,
                    'installments': installments,
                    'amount': total_amount - application_fee
                }
            ]

        # Si viene informacion adicional
        additional_information = [
            'establishment_name'
        ]
        for item in additional_information:
            if item in payment_data.keys():
                body[item] = payment_data[item]

        # Se genera la request
        r = requests.post(self.url + '/payments', headers=self.headers, json=body)
        response = r.json()
        if r.status_code < 400:
            if 'card' in payment_data:
                response['card'] = payment_data['card']
            return self.ok(_format(response), status=r.status_code)
        return self.error(response, status=r.status_code)

    def get(self, payment_id: str):
        filters = {
            'siteOperationId': payment_id,
            'expand': 'card_data'
        }
        r = requests.get(self.url + '/payments', params=filters, headers=self.headers)
        list_results = r.json()['results']
        if len(list_results) == 1:
            return self.ok(_format(list_results[0]), status=r.status_code)
        else:
            return self.error(message='error_pago_no_encontrado', status=r.status_code)

    def search(self, filters: dict) -> dict:
        # El filter puede ser:
        # offset
        # pageSize
        # siteOperationId
        # merchantId
        # dateFrom
        # dateTo
        # site
        r = requests.get(self.url + '/payments', params=filters, headers=self.headers)
        response = r.json()
        response['results'] = [_format(r) for r in response['results']]
        return self.ok(response, status=r.status_code)

    def get_payment_methods(self):
        r = requests.get(self.url + '/payment-methods/1', headers=self.headers)
        return self.ok(r.json(), status=r.status_code)
