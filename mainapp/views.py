from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from mainapp.models import Post, Like, Dislike
from mainapp.serializers import(
    PostSerializer, UserSerializer, 
    DislikeSerializer, LikeSerializer, 
    AuthenticationSeriallizer, RegistrationSerializer
) 

from django.contrib.auth import get_user_model
from mainapp.send_gmail import end_msgs

User = get_user_model()

from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.status import(
    HTTP_200_OK, HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN,
)

from rest_framework.views import APIView


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(methods=['post',], detail=True)
    def set_like(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user
        like = Like.objects.filter(user=user, post=post)
        dislike = Dislike.objects.filter(user=user, post=post)
        if like.exists():
            like.delete()
            return Response({'message': 'Like was deleted'})
        elif dislike.exists():
            dislike.delete()
        Like.objects.create(user=user, post=post)
        return Response({'message': 'you are like this post'})
    
    @action(methods=['post',], detail=True)
    def set_dislike(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user
        like = Like.objects.filter(user=user, post=post)
        dislike = Dislike.objects.filter(user=user, post=post)
        if dislike.exists():
            dislike.delete()
            return Response({'message': 'Like was deleted'})
        elif like.exists():
            like.delete()
        Dislike.objects.create(user=user, post=post)
        return Response({'message': 'you are like this post'})
    

    

class LikeView(ReadOnlyModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    
    @action(methods=['get',], detail=False)
    def get_like(self, request, *args, **kwargs):
        date_from = request.query_params.get('date_from', None)       #запись квери параметров# http://127.0.0.1:8000/api/likes/get_like/?date_from=2023-5-20&date_to=2023-5-30
        date_to= request.query_params.get('date_to', None)


        if date_from == None or date_to == None:
            return Response({'message': 'set data in params'})
        elif date_from == None and date_to == None:
            return Response({'message': 'set data in params'})
        
        like_amount = Like.objects.filter(
            date__gte= date_from, date__lte=date_to
        ).count()
        return Response({'message': like_amount})


class DislikeView(ModelViewSet):
    queryset = Dislike.objects.all()
    serializer_class = DislikeSerializer



class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if User.objects.filter(username=username).exists():
            return Response(
                {'message': 'Пользователь с таким именем сущуствует'},
                status=HTTP_403_FORBIDDEN
            )

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )

        end_msgs(email)

        token = Token.objects.create(user=user)
        return Response({'token': token.key}, HTTP_201_CREATED)

class AuthenticationView(APIView):
    def post(self, request):
        serializer = AuthenticationSeriallizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username=username).first()

        if user is not None:
            if check_password(password, user.password):
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, HTTP_200_OK)
            return Response({'error': 'Пароль не верный'}, HTTP_400_BAD_REQUEST)
        return Response({'error': 'Такого пользователя не существует'}, HTTP_400_BAD_REQUEST)