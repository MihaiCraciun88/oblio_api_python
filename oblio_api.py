import http.client
import urllib.parse
import json
import time
import os


class OblioApi:
    base_url = 'www.oblio.eu'
    cif = ''
    email = ''
    secret = ''
    token_handler = None

    def __init__(self, email, secret, token_handler = None) -> None:
        self.email = email
        self.secret = secret
        if token_handler == None:
            token_handler = OblioApiAccessToken()
        self.token_handler = token_handler

    def set_cif(self, cif) -> None:
        self.cif = cif

    def create_doc(self, type: str, data: dict) -> dict:
        if not 'cif' in data and self.cif != '':
            data['cif'] = self.cif

        if not 'cif' in data:
            raise Exception('Empty cif')

        response = self.request('POST', '/api/docs/{}'.format(type), data)
        self._check_response(response)
        return json.loads(response.read())

    def nomenclature(self, type: str = '', name: str = '', filters: dict = {}) -> dict:
        cif = ''
        if type in ['companies']:
            pass
        elif type in ['companies', 'vat_rates', 'products', 'clients', 'series', 'languages', 'management']:
            cif = self._get_cif()
        else:
            raise Exception('Type not implemented')

        params = {** filters, cif: cif, name: name}
        uri = '/api/nomenclature/{}'.format(type) + '?' + urllib.parse.urlencode(params)

        response = self.request('GET', uri)
        self._check_response(response)
        return json.loads(response.read())
        
    def request(self, method: str, uri: str, payload: dict = {}):
        access_token = self.get_access_token()
        headers = {
            'Host': self.base_url,
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization':  access_token['token_type'] + ' ' + access_token['access_token'],
        }
        conn = http.client.HTTPSConnection(self.base_url)
        conn.request(method, uri, headers = headers, body = json.dumps(payload))
        return conn.getresponse()

    def get_access_token(self) -> dict:
        access_token = self.token_handler.get()
        if access_token == None:
            access_token = self._generate_access_token()
            self.token_handler.set(access_token)
        return access_token

    def _get_cif(self) -> str:
        if self.cif == '':
            raise Exception('Empty cif')
        return self.cif
    
    def _check_response(self, response):
        if response.status < 200 or response.status >= 300:
            message = json.dumps(response.read())
            if message == None:
                message = {
                    'statusMessage': 'Error authorize token! HTTP status: {}'.format(response.status)
                }
            raise Exception(message['statusMessage'], code=response.status)


    def _generate_access_token(self) -> dict:
        if self.email == '' or self.secret == '':
            raise Exception('Email or secret are empty!')

        headers = {
            'Host': self.base_url,
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        payload = {
            'client_id': self.email,
            'client_secret': self.secret,
            'grant_type': 'client_credentials',
        }

        conn = http.client.HTTPSConnection(self.base_url)
        conn.request('POST', '/api/authorize/token', headers = headers, body = json.dumps(payload))
        response = conn.getresponse()
        if response.status < 200 or response.status >= 300:
            raise Exception('Error authorize token! HTTP status: {}'
                .format(response.status), code=response.status)

        return json.loads(response.read())


class OblioApiAccessToken:
    path = ''
    def __init__(self, path = None) -> None:
        if path == None:
            path = 'access_token.json'
        self.path = path

    def get(self) -> dict | None:
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                access_token = json.loads(f.read())
                if access_token != None and access_token['request_time'] + access_token['expires_in'] > int(time.time()):
                    return access_token

        return None

    def set(self, access_token: dict) -> None:
        with open(self.path, 'w') as f:
            f.write(json.dumps(access_token))


if __name__ == '__main__':
    email = ''
    secret = ''
    api = OblioApi(email, secret)
    print(api.nomenclature('companies'))