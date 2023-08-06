from datetime import datetime
import requests
import json
import base64
import urllib.parse
import hashlib
import hmac

class Kyte:
    sessionToken = '0'
    transactionToken = '0'
    username_field = 'email'
    password_field = 'password'

    def __init__(self, public_key, private_key, kyte_account, kyte_identifier, kyte_endpoint):
        self.public_key = public_key
        self.private_key = private_key
        self.kyte_account = kyte_account
        self.kyte_identifier = kyte_identifier
        self.kyte_endpoint = kyte_endpoint

    # create identity string
    def getIdentity(self, timestamp):
        identityStr = self.public_key + "%" + self.sessionToken + "%" + timestamp + "%" + self.kyte_account
        identityStr = base64.b64encode(identityStr.encode("ascii"))
        
        return urllib.parse.quote(identityStr)

    # create kyte signature
    def getSignature(self, epoch):
        # transaction token, set to 0 since we're making a public call
        txToken = '0'
        key1 = hmac.new(self.private_key.encode("utf-8"), txToken.encode("utf-8"), hashlib.sha256).digest()
        # pair 3
        key2 = hmac.new(key1, self.kyte_identifier.encode("utf-8"), hashlib.sha256).digest()
        # signature
        return hmac.new(key2, epoch.encode("utf-8"), hashlib.sha256).hexdigest()

    # make request
    def request(self, method, model, field = None, value = None, data = None, headers = None):
        date = datetime.now()
        epoch = int(date.timestamp())
        timestamp = datetime.utcfromtimestamp(epoch).strftime('%a, %d %b %Y %H:%M:%S GMT')
        signature = self.getSignature(str(epoch))
        identity = self.getIdentity(timestamp)

        endpoint = self.kyte_endpoint + "/" + model
        if field is not None and value is not None:
            endpoint += "/" + field + "/" + value

        # prepare headers
        _headers={
            'Content-Type':'application/json',
            'Accept':'application/json',
            'x-kyte-signature':signature,
            'x-kyte-identity':identity
        }
        _headers.update(headers)

        try:
            # execute request based on method
            if method == "post":
                # post request
                r = requests.post(endpoint, json=json.dumps(data), headers=_headers)
            elif method == "put":
                r = requests.put(endpoint, json=json.dumps(data), headers=_headers)
            elif method == "get":
                r = requests.get(endpoint, headers=_headers)
            elif method == "delete":
                r = requests.delete(endpoint, headers=_headers)
            else:
                raise Exception("Unknown method {} was called. Supported methods are POST, PUT, GET, and DELETE".format(method))

            if r.status_code != 200:
                if r.status_code == 400:
                    raise Exception("400 Bad request for {}: {}").format(method, endpoint)
                elif r.status_code == 404:
                    raise Exception("404 Unknown for {}: {}").format(method, endpoint)
                elif r.status_code == 403:
                    raise Exception("403 Access denied for {}: {}").format(method, endpoint)
                elif r.status_code >= 500:
                    raise Exception("{} Server-side error... {}: {}").format(r.status_code, method, endpoint)
                else:
                    raise Exception("{} ERROR {}: {}").format(r.status_code, method, endpoint)

        except requests.exceptions.Timeout:
            raise Exception("Connection timed out for {}: {}".format(method, endpoint))
        except requests.exceptions.TooManyRedirects:
            raise Exception("Too many redirects for {}: {}".format(method, endpoint))
        except requests.exceptions.HTTPError as e:
            raise Exception("Fatal Error: {}. Attempted {}: {}".format(e, method, endpoint))
        
        # update session and tx tokens
        self.sessionToken = r.json().get('session')
        self.transactionToken = r.json().get('token')

        # return json dictionary
        return r.json()

    # make post request
    def post(self, model, data, headers):
        result = self.request("post", model, None, None, data, headers)
        return result

    def put(self, model, field, value, data, headers):
        result = self.request("put", model, field, value, data, headers)
        return result

    def get(self, model, field, value, headers):
        result = self.request("get", model, field, value, headers)
        return result

    def delete(self, model, field, value, headers):
        result = self.request("delete", model, field, value, headers)
        return result

    def createSession(self, username, password):
        result = self.post("Session", {self.username_field:username, self.password_field:password}, {})
        self.sessionToken = result.get('sessionToken')
        self.transactionToken = result.get('txToken')
        return result
