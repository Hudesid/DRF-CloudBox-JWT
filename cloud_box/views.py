from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import BasePermission, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt.tokens import RefreshToken
from . import serializers, models


class UserCreateAPIView(CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class AuthorValidateAPIView(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class UserUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [AuthorValidateAPIView or IsAdminUser]


class FolderListCreateAPIView(ListCreateAPIView):
    queryset = models.Folder.objects.all()
    serializer_class = serializers.FolderSerializer
    permission_classes = [IsAuthenticated or IsAdminUser]
    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ['folder_name', 'created_at']
    ordering = ['folder_name']
    search_fields = ['^folder_name', '=created_at']


class FolderRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.Folder.objects.all()
    serializer_class = serializers.FolderSerializer
    permission_classes = [AuthorValidateAPIView or IsAdminUser]


class FileListCreateAPIView(ListCreateAPIView):
    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer
    permission_classes = [IsAuthenticated or IsAdminUser]
    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ['file_name', 'file', 'uploaded_at']
    ordering = ['file']
    search_fields = ['^file_name', '=file']

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data.copy()
        data['user'] = user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer
    permission_classes = [AuthorValidateAPIView or IsAdminUser]

    def delete(self, request, *args, **kwargs):
        file_to_delete = self.get_object()
        file_to_delete.is_deleted = True
        file_to_delete.save()
        return Response({"detail": "File moved to trash."}, status=status.HTTP_204_NO_CONTENT)


# class TrashListAPIView(ListAPIView):
#     queryset = models.Trash.objects.all()
#     serializer_class = serializers.TrashSerializer
#     permission_classes = [IsAuthenticated or IsAdminUser]
#     filter_backends = [SearchFilter, OrderingFilter]
#     search_fields = ['^file__file_name', '=deleted_at']
#     ordering_fields = ['file__folder', 'deleted_at']
#     ordering = ['deleted_at']
#
#
# class TrashRetrieveDestroyAPIView(RetrieveDestroyAPIView):
#     queryset = models.Trash.objects.all()
#     serializer_class = serializers.TrashSerializer
#     permission_classes = [IsAuthenticated or IsAdminUser]
#
#     @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated or IsAdminUser])
#     def restore(self, request, *args, **kwargs):
#         trash_item = self.get_object()
#
#         file_to_restore = trash_item.file
#
#         if models.File.objects.filter(id=file_to_restore.id).exists():
#             return Response({"detail": "The file already exists."}, status=status.HTTP_400_BAD_REQUEST)


class TrashListAPIView(ListAPIView):
    queryset = models.File.objects.all()
    serializer_class = serializers.TrashSerializer
    permission_classes = [IsAuthenticated or IsAdminUser]
    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ['file_name', 'file', 'uploaded_at']
    ordering = ['file']
    search_fields = ['^file_name', '=file']


class TrashRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    queryset = models.File.objects.all()
    serializer_class = serializers.TrashSerializer
    permission_classes = [IsAuthenticated or IsAdminUser]


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."})
        except KeyError:
            return Response({"detail": "Refresh token required."})

