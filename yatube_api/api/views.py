from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from posts.models import Group, Post, Comment
from .serializers import CommentSerializer, GroupSerializer, PostSerializer
from .mixins import UpdateDeleteViewSet


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(UpdateDeleteViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(UpdateDeleteViewSet):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, pk=post_id)
        new_queryset = post.comments.all()
        return new_queryset

    def get_object(self):
        post_id = self.kwargs.get("post_id")
        comment_id = self.kwargs.get("pk")
        obj = get_object_or_404(Comment, id=comment_id, post=post_id)
        return obj
