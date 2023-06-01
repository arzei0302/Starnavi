from django.urls import path
from rest_framework.routers import DefaultRouter
from mainapp.views import (
    PostView, UserView, LikeView, DislikeView,
    RegistrationView, AuthenticationView
)


router = DefaultRouter()

router.register('posts', PostView, basename='post')
router.register('user',UserView, basename='user' )
router.register('likes',LikeView, basename='like' )
router.register('dislikes',DislikeView, basename='dislike' )


urlpatterns = [
    path('reg/', RegistrationView.as_view()),
    path('aut/', AuthenticationView.as_view())
]

urlpatterns += router.urls