import json
import urllib
from aiohttp import ClientSession


class Entity:
    instance = None

    def __init__(self, fulldomain, auth):
        self.fulldomain = fulldomain
        self.auth = auth

    def __new__(cls, fulldomain, auth):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    async def _get_headers(self):
        return {
            "Authorization": await self.auth.get_access_token(),
            "User-Agent": "amoCRM-oAuth-client/1.0"
        }

    async def get(self, url, params={}):
        try:
            if params:
                query_url = f'{url}?{urllib.parse.urlencode(params)}'
            else:
                query_url = url
            async with ClientSession() as session:
                async with session.get(url=query_url, headers=await self._get_headers()) as response:
                    req = await response.text()
        except Exception:
            raise
            # return {'result': False, 'message': 'Переданы неверные данные'}
        return self.__parse_request_object_async({'status_code': response.status, 'data': req})

    async def post(self, url, post_data, is_delete=False):
        async with ClientSession() as session:
            async with session.post(url=url, headers=await self._get_headers(), json=post_data) as response:
                responser = await response.text()
        return self.__parse_request_object_async({'status_code': response.status, 'data': responser}, is_delete)

    async def patch(self, url, edit_data):
        async with ClientSession() as session:
            async with session.patch(url=url, headers=await self._get_headers(), json=edit_data) as response:
                responser = await response.text()
        return self.__parse_request_object_async({'status_code': response.status, 'data': responser})

    async def delete(self, url):
        async with ClientSession() as session:
            async with session.delete(url=url, headers=await self._get_headers()) as response:
                responser = await response.text()
        return self.__parse_request_object_async({'status_code': response.status, 'data': responser}, True)

    def __parse_request_object_async(self, request_object, is_delete=False):
        success_code = 200 if not is_delete else 204
        result = {'result': request_object['status_code'] == success_code}
        try:
            result['data'] = json.loads(request_object['data'])
        except Exception:
            result['data'] = request_object['data']
        if not result['result']:
            result['status_code'] = request_object['status_code']
        return result
