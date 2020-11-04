from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.permissions import SAFE_METHODS
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from engine.serializers import PostsSerializer
from engine.models import Posts, PostLikes


class PostViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all().order_by('-id')
    serializer_class = PostsSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['POST'])
    def like(self, request, pk):
        """
            Здесь логика была следующей. Я думаю, что вью не должна возвращать
            одинаковый респонс(пост+200) при выполнении разных действий(like/unlike). Также нужно было решить проблему
            с тем, что функция не должна выполнять два разных(даже противоположных) действия like/unlike
            Я решил вынести логику во вью и разделить в итоге у поста есть две функции выполняющие свое предназначение,
            а сама вью возвращает результат зависящий от выполненного дейтсвия.

            PS. Это можно также было разделить на фронте и создать две вью /posts/1/like & /posts/1/unlike
            (может тоже жизнеспособный вариант)

        """
        post = self.get_object()

        like = post.likes.filter(owner=request.user).first()
        if like:
            post.unlike(like)
            response_status = status.HTTP_204_NO_CONTENT
        else:
            post.like(owner=request.user)
            response_status = status.HTTP_200_OK
        serializer = self.get_serializer(post)
        return Response(data=serializer.data, status=response_status)
