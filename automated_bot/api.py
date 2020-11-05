import requests
from requests.exceptions import HTTPError

from auth import CustomAuth


class SocialNetworkApi:
    def __init__(self, api_url):
        self._api_url = api_url

    def post_request(self, path, data=None, auth=None):
        try:
            response = requests.post(f'{self._api_url}{path}', data=data, auth=auth)
            response.raise_for_status()
        except HTTPError as e:
            raise Exception(e)
        return response.json()


class UserSocialNetworkApi(SocialNetworkApi):
    def __init__(self, api_url, auth=None):
        self.auth = auth
        super(UserSocialNetworkApi, self).__init__(api_url)

    def signup(self, data):
        path = '/user/signup/'
        self.post_request(path=path, data=data)

    def login(self, credentials):
        token = self._get_token(credentials)
        self.auth = CustomAuth(token)

    def _get_token(self, credentials):
        path = '/user/login/'
        response = self.post_request(path=path, data=credentials)
        return response['token']


class PostSocialNetworkApi(SocialNetworkApi):
    def __init__(self, api_url):
        self._db_id = None
        super(PostSocialNetworkApi, self).__init__(api_url)

    def create(self, data, auth):
        path = '/api/posts/'
        response_data = self.post_request(path=path, data=data, auth=auth)
        self._db_id = response_data['id']

    def like(self, owner, auth):
        path = f'/api/posts/{self._db_id}/like/'
        self.post_request(path=path, auth=auth)

