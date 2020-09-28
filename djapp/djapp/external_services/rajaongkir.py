import requests

from djapp.config import Config


class RajaOngkir():
    cfg = Config.GetConfig()
    endpoint = cfg['rajaongkir']['endpoint']
    apikey = cfg['rajaongkir']['apikey']

    @classmethod
    def setup(cls, initdata={}):
        cls.endpoint = initdata['endpoint']
        cls.apikey = initdata['apikey']
        return cls

    @classmethod
    def api_get(cls, path=''):
        endpoint = cls.endpoint + path
        responses = requests.get(endpoint, params={'key': cls.apikey})
        geodata = responses.json()
        return geodata

    @classmethod
    def get_city(cls, args=None):
        result = cls.api_get(args['path'])
        return result
