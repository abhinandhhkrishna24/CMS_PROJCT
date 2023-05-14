from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import  Post, Like , AccoutUser
from .permissions import IsAdminUserOrReadOnly # <-- Add this line
from .serializers import AccountUserSerializer, PostSerializer, LikeSerializer 




class UserListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = AccountUserSerializer
    queryset = AccoutUser.objects.all()


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccountUserSerializer
    queryset = AccoutUser.objects.all()
    lookup_field = 'username'



class PostListCreateView(LoginRequiredMixin, generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(is_public=True) | Post.objects.filter(author=self.request.user).order_by('-created_at')
        else:
            return Post.objects.filter(is_public=True).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUserOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(author=self.request.user)
        else:
            return Post.objects.filter(is_public=True)

    def perform_update(self, serializer):
        post = self.get_object()
        if post.author != self.request.user:
            raise PermissionDenied("You can't update this post.")
        serializer.save()


class LikeCreateView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        like = Like(post=post, user=request.user)
        like.save()
        serializer = self.serializer_class(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LikeDestroyView(generics.DestroyAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        like = get_object_or_404(Like, post=post, user=request.user)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
