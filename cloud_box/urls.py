from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('auth/register/', views.UserCreateAPIView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/user/detail/<int:pk>/', views.UserUpdateAPIView.as_view(), name='user_detail'),
    path('auth/folder/list/', views.FolderListCreateAPIView.as_view(), name='folder_list'),
    path('auth/folder/detail/<int:pk>/', views.FolderRetrieveUpdateDestroyAPIView.as_view(), name='folder_detail'),
    path('auth/file/list/', views.FileListCreateAPIView.as_view(), name='file_list'),
    path('auth/file/detail/<int:pk>/', views.FileRetrieveUpdateDestroyAPIView.as_view(), name='file_detail'),
    path('auth/trash/list/', views.TrashListAPIView.as_view(), name='trash_list'),
    path('auth/trash/detail/<int:pk>/', views.TrashRetrieveDestroyAPIView.as_view(), name='trash_detail')
]