from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import UserListCreateView, UserRetrieveUpdateDestroyView, PostListCreateView, \
    PostRetrieveUpdateDestroyView, LikeCreateView, LikeDestroyView

app_name = 'cms_app'

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/users/', UserListCreateView.as_view(), name='user_list_create'),
    path('api/users/<str:username>/', UserRetrieveUpdateDestroyView.as_view(), name='user_retrieve_update_destroy'),

    path('api/posts/', PostListCreateView.as_view(), name='post_list_create'),
    path('api/posts/<uuid:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post_retrieve_update_destroy'),

    path('api/posts/<uuid:post_id>/like/', LikeCreateView.as_view(), name='like_create'),
    path('api/posts/<uuid:post_id>/unlike/', LikeDestroyView.as_view(), name='like_destroy'),
]
