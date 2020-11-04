from requests.auth import AuthBase


class CustomAuth(AuthBase):
    def __init__(self, token):
        self._token = token

    def __call__(self, request):
        request.headers['Authorization'] = 'Bearer %s' % self._token
        return request
