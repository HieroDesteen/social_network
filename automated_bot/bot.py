import random
import string
import logging
import logging.config
import sys

import yaml
import collections

from api import UserSocialNetworkApi, PostSocialNetworkApi

Like = collections.namedtuple('Like', ['owner'])


class User:
    def __init__(self, email, api_url, password=None):
        self.email = email
        self.password = password if password else self._make_random_password()
        self._api = UserSocialNetworkApi(api_url)
        self._api_url = api_url
        self.posts = []
        self.setted_likes = 0

    def signup(self):
        self._api.signup({"email": self.email, "password": self.password})

    def login(self):
        self._api.login({"email": self.email, "password": self.password})

    def create_post(self, text=None):
        post = Post(self, self._api_url, text)
        post.create(self._api.auth)
        self.posts.append(post)

    def send_like(self, post):
        post.like(owner=self, user_auth=self._api.auth)
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
        self._api = PostSocialNetworkApi(api_url)
        self.text = text if text else self._get_text()
        self.likes = []
        self._post_id = None

    @staticmethod
    def _get_text():
        return "Hello World!"

    def create(self, user_auth):
        data = {"text": self.text}
        self._api.create(data=data, auth=user_auth)

    def like(self, owner, user_auth):
        self._api.like(owner, user_auth)
        like = Like(owner=owner)
        self.likes.append(like)


class AutomatedBot:
    def __init__(self):
        self.config = self._read_configurations()
        self._url = self.config['site_url']
        self._users = []

    def start(self):
        logging.info(' Bot started '.center(60, '*'))
        logging.info(' Start users initializing '.center(60, '*'))
        self.init_users()
        for user in self._users:
            user.login()
            self.create_posts(user)
        logging.info(' Start likes activity by users '.center(60, '*'))
        self.likes_engine()

    def likes_engine(self):
        try:
            sender = self._get_curr_user()
            logging.info(f' Start likes activity by user {sender.email} '.center(60, '*'))
            for i in range(self.config['max_likes_per_user']):
                receiver = self._get_user_with_zero_likes(sender)
                self._send_like_by_user(sender, receiver)
            self.likes_engine()
        except Exception as e:
            logging.error(e)

    def _send_like_by_user(self, sender, receiver):
        post = self._get_post(sender, receiver.posts)
        sender.send_like(post)
        logging.info(f'User {sender.email} send like for user {receiver.email}')

    def _get_post(self, sender, posts):
        post = random.choice(posts)
        if sender not in [like.owner for like in post.likes]:
            return post
        return self._get_post(sender, posts)

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
        logging.info(f'Creation of {posts_count} posts for user {user.email} started')
        for i in range(posts_count):
            user.create_post()
            logging.info(f'Post {i} created.')

    def init_users(self):
        for k in range(0, self.config['number_of_users']):
            email = f'test{k}@gmail.com'
            user = User(email, self._url)
            user.signup()
            self._users.append(user)
            logging.info(f'User {email} created.')

    @staticmethod
    def _read_configurations():
        with open('bot_config.yaml') as fh:
            cfg = yaml.load(fh, Loader=yaml.FullLoader)
        return cfg['settings']


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s', handlers=[
        logging.FileHandler("automated_bot.log"),
        logging.StreamHandler()
    ])
    bot = AutomatedBot()
    bot.start()


if __name__ == '__main__':
    main()
