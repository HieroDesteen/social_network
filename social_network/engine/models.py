from django.db import models

from users.models import User


class Posts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    text = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    @property
    def likes_count(self):
        return self.likes.all().count()

    def like(self, owner):
        like = PostLikes(owner=owner, post=self)
        like.save()

    @staticmethod
    def unlike(like):
        like.delete()


class PostLikes(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='likes', null=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('owner', 'post')
