import requests
from .models.model import ClientModel

class RequestClient(ClientModel):
    '''cache client is a client model that is used to store data in a cache file'''
    def __init__(self, *args, headers=None, **kwargs):
        self.dict = {}
        if not headers:
            self.headers = {'Content-Type': 'application/json'}
        elif isinstance(headers, dict):
            self.headers = headers
        else:
            raise Exception("headers must be a dict") from None
        super().__init__(self.dict, *args, **kwargs)

    def get(self, url, **kwargs):
        '''get the data from the url'''
        headers = kwargs.get('headers', self.headers)
        data = kwargs.get('data', None)
        auth = kwargs.get('auth', None)
        return requests.get(url, headers=headers, data=data, auth=auth)

    def post(self, url, **kwargs):
        '''post the data to the url'''
        headers = kwargs.get('headers', self.headers)
        data = kwargs.get('data', None)
        return requests.post(url, headers=headers, data=data)

    def delete(self, url, **kwargs):
        '''delete the data from the url'''
        headers = kwargs.get('headers', self.headers)
        data = kwargs.get('data', None)
        return requests.delete(url, headers=headers, data=data)

    def put(self, url, **kwargs):
        '''put the data to the url'''
        headers = kwargs.get('headers', self.headers)
        data = kwargs.get('data', None)
        return requests.put(url, headers=headers, data=data)
