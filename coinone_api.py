import httplib2
import time
import simplejson as json
import base64
import hmac
import hashlib

# 전역변수 설정
ACCESS_TOKEN = '자신이 받은 Access Token 입력'
SECRET_KEY = '자신이 받은 Secret Key 입력'


def get_encoded_payload(payload):
    payload[u'nonce'] = int(time.time() * 1000)

    dumped_json = json.dumps(payload).encode()
    encoded_json = base64.b64encode(dumped_json)
    return encoded_json


def get_signature(encoded_payload, secret_key):
    signature = hmac.new(secret_key.upper().encode(), encoded_payload, hashlib.sha512);
    return signature.hexdigest()


def get_response(url, payload):
    encoded_payload = get_encoded_payload(payload)
    headers = {
        'Content-type': 'application/json',
        'X-COINONE-PAYLOAD': encoded_payload,
        'X-COINONE-SIGNATURE': get_signature(encoded_payload, SECRET_KEY)
    }
    http = httplib2.Http()
    response, content = http.request(url, 'GET', headers=headers, body=encoded_payload)
    return content


def post_response(url, payload):
    encoded_payload = get_encoded_payload(payload)
    headers = {
        'Content-type': 'application/json',
        'X-COINONE-PAYLOAD': encoded_payload,
        'X-COINONE-SIGNATURE': get_signature(encoded_payload, SECRET_KEY)
    }
    http = httplib2.Http()
    response, content = http.request(url, 'POST', headers=headers, body=encoded_payload)
    return content


def coin_balance():
    url = 'https://api.coinone.co.kr/v2/account/balance/'
    payload = {
        "access_token": ACCESS_TOKEN,
    }
    content = post_response(url, payload)
    return content


def coin_order_book(currency):
    url = 'https://api.coinone.co.kr/orderbook/?currency={}&format=json'.format(currency)
    payload = {
        "access_token": ACCESS_TOKEN,
    }
    content = get_response(url, payload)
    return content


def coin_limit_buy(price, qty, currency):
    url = 'https://api.coinone.co.kr/v2/order/limit_buy/'
    payload = {
        "access_token": ACCESS_TOKEN,
        "price": price,
        "qty": qty,
        "currency": currency
    }
    content = post_response(url, payload)
    return content


def coin_limit_sell(price, qty, currency):
    url = 'https://api.coinone.co.kr/v2/order/limit_sell/'
    payload = {
        "access_token": ACCESS_TOKEN,
        "price": price,
        "qty": qty,
        "currency": currency
    }
    content = post_response(url, payload)
    return content
