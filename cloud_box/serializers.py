from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'email', 'password')

    def create(self, validated_data):
        user = models.User.objects.create(**validated_data)
        password = validated_data['password']
        user.set_password(password)
        user.save()
        return user


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Folder
        fields = ('id', 'folder_name', 'parent_folder', 'created_at')


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.File
        fields = ('id', 'file_name', 'file', 'file_size', 'uploaded_at', 'updated_at', 'user', 'folder')


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        representation['folder'] = FolderSerializer(instance.folder).data
        return representation

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        if 'user' in data:
            try:
                user = models.User.objects.get(id=data['user'])
                internal_value['user'] = user
            except models.User.DoesNotExist:
                raise serializers.ValidationError({'user': 'Invalid user ID.'})
        if 'folder' in data:
            try:
                folder = models.Folder.objects.get(id=data['folder'])
                internal_value['folder'] = folder
            except models.Folder.DoesNotExist:
                raise serializers.ValidationError({'folder': 'Invalid folder ID.'})
        return internal_value




class TrashSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Trash
        fields = ('id', 'file', 'deleted_at')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['file'] = UserSerializer(instance.file).data
        return representation