from rest_framework import serializers
from .models import AccoutUser, Post, Like , User



class AccountUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(source='user.password', write_only=True)
    
    class Meta:
        model = AccoutUser
        fields = ['name', 'date_of_birth', 'username', 'email', 'password']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()
        account_user = AccoutUser.objects.create(user=user, **validated_data)
        return account_user

class PostSerializer(serializers.ModelSerializer):
    number_of_likes = serializers.SerializerMethodField()
    owner = AccountUserSerializer(read_only=True)

    def get_number_of_likes(self, obj):
        return obj.like_set.count()

    class Meta:
        model = Post
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'