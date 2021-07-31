from django.http.response import JsonResponse
from home.serializer import BlogModelSerializer
from django.shortcuts import render,  redirect
from .serializer import BlogModelSerializer, UserSerializer
from .models import BlogModel
from rest_framework.response import Response
from rest_framework import generics, serializers, status, viewsets
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from .verify import JWTAuthentication
from .form import BlogForm
from rest_framework.decorators import action, permission_classes, authentication_classes
import jwt
from rest_framework import exceptions
from django.conf import settings
from django.contrib.auth import get_user_model

def home(request):
    return render(request, 'home.html')

def signin(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'register.html')

def logout(request):
    return render(request, 'end.html')

def myaccount(request):
    return render(request, 'account.html')

def allblogs(request):
    blogs = BlogModel.objects.all()
    b = list()
    ids = list()
    titles = list()
    contents = list()
    users = list()
    votes = list()
    for i in blogs:
        b.append({
            'id' : i.id,
            'photo' : i.image,
            'title' : i.title,
            'content' : i.content,
            'user' : i.user.username,
            'votes' : i.votes
        })
        ids.append(i.id)
        titles.append(i.title)
        contents.append(i.content)
        users.append(i.user.username)
        votes.append(i.votes)
    length = len(ids)
    return render(request, 'index.html', context={'ids' : ids, 'titles' : titles, 'contents' : contents, 'users' : users, 'votes' : votes, 'len' : length, 'b' : b})
    
def openblog(request, id):
    blog = BlogModel.objects.filter(id=id)
    print(blog[0])
    blog = blog[0]
    return render(request, 'blog.html', context={"blogid" : id, "votes" : blog.votes, "title" : blog.title, "content" : blog.content, "author" : blog.user.username, "created_at" : blog.created_at, "updated_at" : blog.upload_to, "photo" : blog.image})

def getuser(request):
    authorization_heaader = request.headers.get('Authorization')
    if not authorization_heaader:
            return None
    try:
        access_token = authorization_heaader.split(' ')[1]
        payload = jwt.decode(
            access_token, settings.SECRET_KEY, algorithms=['HS256'])

    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed('access_token expired')
    except IndexError:
        raise exceptions.AuthenticationFailed('Token prefix missing')

    user = User.objects.filter(id=payload['user_id']).first()
    return JsonResponse({'username' : user.username, 'email' : user.email})

def updateblog(request, id):
    blog = BlogModel.objects.get(id=id)
    try:
        if request.method == 'POST':
            User = get_user_model()
            form = BlogForm(request.POST)
            try:
                blog.image = request.FILES['image']
            except:
                print("No IMage")

            
            blog.title = request.POST.get('title')
            access_token = request.POST['access']
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])
            blog.user = User.objects.filter(id=payload['user_id']).first()
            if form.is_valid():
                blog.content = form.cleaned_data['content']
            blog.save()
            return redirect('myblogs')
    except Exception as e :
        print(e)
    
    return render(request, 'updateblog.html', context={"blogid" : id, 'form' : BlogForm(instance=blog)})


def createblog(request):
    try:
        if request.method == 'POST':
            User = get_user_model()
            form = BlogForm(request.POST)
            image = request.FILES['image']
            title = request.POST.get('title')
            access_token = request.POST['access']
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])
            
            user = User.objects.filter(id=payload['user_id']).first()
            
            if form.is_valid():
                content = form.cleaned_data['content']
            
            blog_obj = BlogModel.objects.create(
                user = user , title = title, votes=0,
                content = content, image = image
            )
            return redirect('allblogs')
    except Exception as e :
        print(e)
    return render(request, 'createblog.html', context={'form' : BlogForm})

def myblogs(request, id):
    blogs = BlogModel.objects.all()
    b = list()
    ids = list()
    titles = list()
    contents = list()
    users = list()
    votes = list()
    # print(blogs)
    for i in blogs:
        if i.user.id == id: 
            b.append({
                'id' : i.id,
                'photo' : i.image,
                'title' : i.title,
                'content' : i.content,
                'user' : i.user.username,
                'votes' : i.votes
            })
    length = len(b)
    return render(request, 'myblogs.html', context={ 'len' : length, 'b' : b})


class BlogModelListView(generics.ListAPIView, generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    model=BlogModel
    queryset = BlogModel.objects.all()
    serializer_class = BlogModelSerializer

class BlogModelDetailViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    model=BlogModel
    queryset = BlogModel.objects.all()
    serializer_class = BlogModelSerializer

    @csrf_exempt
    @action(detail=True, methods=['POST'])
    def voter(self, request, pk):
        blog = self.get_object()
        user = request.user
        items= blog.voted.all()
        if user in items:
            blog.votes = blog.votes - 1
            blog.voted.remove(user)
            blog.save()
            return Response({'votes' : blog.votes})
        blog.voted.add(user)
        blog.votes = blog.votes + 1
        blog.save()
        return Response({'votes' : blog.votes})
        
    def post(self, request):
        try:
            form = BlogForm(request.POST)
            image = request.FILES['image']
            title = request.POST.get('title')
            au = JWTAuthentication()
            user = au.authenticate(request)
                
            if form.is_valid():
                content = form.cleaned_data['content']
                
                blog_obj = BlogModel.objects.create(
                    user = user , title = title, 
                    content = content, image = image
                )
                return render(request, 'blogs')
        except Exception as e :
            print(e)
        return render(request, 'createblog.html', context={'form' : BlogForm})


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    @authentication_classes(JWTAuthentication)
    @permission_classes(IsAuthenticated)
    def aboutme(self, request, pk):
        au = JWTAuthentication()
        user = au.authenticate(request)
        uid = user[0].id
        return Response({'id' : uid})


