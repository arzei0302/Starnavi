from rest_framework import serializers, exceptions
from mainapp.models import Post, Like, Dislike
from django.contrib.auth import get_user_model

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id', 'user', 'timestamp', 'content'
        )


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            'id', 'user', 'date', 'post',
        )



class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = (
            'id', 'user', 'timestamp', 'post',
        )


class UserSerializer(serializers.ModelSerializer):
    posts = PostSerializer(read_only=True, many=True)
    likes = LikeSerializer(read_only=True, many=True)
    dislikes = DislikeSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = (
            'id', 'groups', 'user_permissions',
            'posts', 'likes', 'dislikes',
        )


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()

    def validated_password(self, value):
        if len(value) < 6:
            raise exceptions.ValidationError('Пароль слишком короткий')                  
        elif len(value) > 20:
            raise exceptions.ValidationError('Пароль слишком длинный')
        return value

class AuthenticationSeriallizer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()






{
    "username": "arz",
    "email": "arzeiarzeiarzeiarzei@gmail.com",
    "password": "arz1234"
    
}


