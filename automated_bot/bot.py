import random
import string

import yaml
import requests
import collections

from auth import CustomAuth

Like = collections.namedtuple('Like', ['owner'])


class User:
    def __init__(self, email, api_url, password=None):
        self.email = email
        self.password = password if password else self._make_random_password()
        self._api_url = api_url
        self.posts = []
        self.setted_likes = 0
        self._auth = None

    def signup(self):
        response = requests.post(f'{self._api_url}/user/signup/', data={"email": self.email,
                                                                        "password": self.password
                                                                        })
        if response.status_code != requests.codes.created:
            raise Exception('User not created.')

    def login(self):
        token = self._get_token()
        self._auth = CustomAuth(token)

    def _get_token(self):
        response = requests.post(f'{self._api_url}/user/login/', data={"email": self.email,
                                                                       "password": self.password
                                                                       })
        data = response.json()
        return data['token']

    def create_post(self, text=None):
        post = Post(self, self._api_url, text)
        post.create(self._auth)
        self.posts.append(post)

    def set_like(self, post):
        post.like(owner=self, user_auth=self._auth)
        self.setted_likes += 1

    @staticmethod
    def _make_random_password():
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(8))

    @property
    def posts_count(self):
        return len(self.posts)

    @property
    def likes_count(self):
        return sum([len(post.likes) for post in self.posts])

    @property
    def is_zero_liked_post(self):
        return not all([post.likes for post in self.posts])


class Post:
    def __init__(self, author, api_url, text=None):
        self.author = author
        self._api_url = api_url
        self.text = text if text else self._get_text()
        self.likes = []
        self._id = None

    @staticmethod
    def _get_text():
        return "Hello World!"

    def create(self, user_auth):
        response = requests.post(f'{self._api_url}/api/posts/', data={"text": self.text}, auth=user_auth)
        if response.status_code != requests.codes.created:
            raise Exception('Post not created.')
        self._id = response.json()['id']

    def like(self, owner, user_auth):
        response = requests.post(f'{self._api_url}/api/posts/{self._id}/like/', auth=user_auth)
        if response.status_code != requests.codes.ok:
            raise Exception('Like not created.')
        like = Like(owner=owner)
        self.likes.append(like)


class AutomatedBot:
    def __init__(self):
        self.config = self._read_configurations()
        self._url = self.config['site_url']
        self._users = []

    def start(self):
        self.init_users()
        for user in self._users:
            user.login()
            self.create_posts(user)
        self.likes()

    def likes(self):
        try:
            curr_user = self._get_curr_user()
            post = self._get_user_post(curr_user)
            if curr_user not in [like.owner for like in post.likes]:
                curr_user.set_like(post)
            self.likes()
        except Exception as e:
            print(e)

    def _get_user_post(self, curr_user):
        user = self._get_user_with_zero_likes(curr_user)
        return random.choice(user.posts)

    def _get_user_with_zero_likes(self, curr_user):
        users_list = sorted(self._users, key=lambda u: not u.is_zero_liked_post)
        users_list.remove(curr_user)
        user = users_list[0] if users_list else None
        if user is None or not user.is_zero_liked_post:
            raise Exception("Bot stopped.")
        return user

    def _get_curr_user(self):
        users_list = [user for user in self._users if user.setted_likes < self.config['max_likes_per_user']]
        if not users_list:
            raise Exception('Bot stopped.')
        users_list = sorted(users_list, key=lambda u: (u.posts_count, -u.likes_count), reverse=True)
        return users_list[0]

    def create_posts(self, user):
        posts_count = random.randrange(1, self.config['max_posts_per_user'])
        for i in range(posts_count):
            user.create_post()

    def init_users(self):
        for k in range(0, self.config['number_of_users']):
            email = f'test{k}@gmail.com'
            user = User(email, self._url)
            user.signup()
            self._users.append(user)

    @staticmethod
    def _read_configurations():
        with open('bot_config.yaml') as fh:
            cfg = yaml.load(fh, Loader=yaml.FullLoader)
        return cfg['settings']


def main():
    bot = AutomatedBot()
    bot.start()


if __name__ == '__main__':
    main()
