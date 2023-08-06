from datetime import datetime
from json import dumps
from os import environ

import requests
from pytz import timezone
from requests.models import Response


class UnousRequests:

    def __init__(self, show_log=True):
        self.show_log = show_log

    def get(
        self,
        url,
        headers={},
        params=None,
        data={},
        json=None,
        timeout=int(environ.get('TIMEOUT_REQUISICAO_UNOUS', 10)),
    ):
        try:
            return requests.get(
                url=url,
                headers=headers,
                params=params,
                json=json,
                data=data,
                timeout=timeout,
            )
        except Exception as e:
            return self.create_error_response(e, 'GET', url)

    def post(
        self,
        url,
        headers={},
        params=None,
        data={},
        json=None,
        timeout=int(environ.get('TIMEOUT_REQUISICAO_UNOUS', 10)),
    ):
        try:
            return requests.post(
                url=url,
                headers=headers,
                params=params,
                data=data,
                json=json,
                timeout=timeout,
            )
        except Exception as e:
            return self.create_error_response(e, 'POST', url)

    def create_error_response(self, error, method, url):
        erro, agora = error.__class__.__name__, datetime.now(tz=timezone('America/Sao_Paulo'))
        log = f'{agora}: Um {erro} ocorreu ao executar um {method} na url {url}.'
        response = Response()
        response.encoding = 'utf-8'
        response.status_code = 408
        response.url = url
        response._content = dumps({'erro': log[34:]}).encode('utf-8')
        print(log) if self.show_log else None
        return response
