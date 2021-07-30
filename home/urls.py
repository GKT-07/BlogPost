from django.urls import path, include
from .views import BlogModelListView, BlogModelDetailViewSet, allblogs, home, logout, myaccount, signin, signup, UserViewSet, openblog, createblog, myblogs, allblogs, updateblog, getuser
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

router = routers.DefaultRouter()
router.register('register', UserViewSet)
router.register('signup/register', UserViewSet)
router.register('openblog/register', UserViewSet)
router.register('openblog/blogs', BlogModelDetailViewSet)
router.register('vote/blogs', BlogModelDetailViewSet)
router.register('openblog/vote/blogs', BlogModelDetailViewSet)
router.register('createblog/blogs', BlogModelDetailViewSet)
router.register('vote/blogs', BlogModelDetailViewSet)
router.register('myblogs/blogs',BlogModelDetailViewSet)
router.register('update/blogs',BlogModelDetailViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('signin', signin, name='signin'),
    path('signup', signup, name='signup'),
    path('allblogs', allblogs, name='allblogs'),
    path('myblogs', myblogs, name='myblogs'),
    path('openblog/<int:id>', openblog, name='seeblog'),
    path('createblog', createblog, name='createblog'),
    path('update/<int:id>', updateblog, name='updateblog'),
    path('blogs', BlogModelListView.as_view()),
    path('auth/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('logout', logout, name='logout'),
    path('openblog/logout', home, name='logout'),
    path('allblogs/logout', home, name='logout'),
    path('createblog/logout', home, name='logout'),
    path('myblogs/logout', home, name='logout'),
    path('myaccount', myaccount, name='myaccount'),
    path('update/logout', home, name='logout'),
    path('myaccount/logout', home, name='logout'),
    path('openblog/auth/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('update/auth/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('myaccount/auth/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('myblogs/auth/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('createblog/auth/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('allblogs/auth/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('getuser', getuser, name='getusers'),
    path('', include(router.urls))
]