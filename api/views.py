from django.shortcuts import render
from rest_framework.viewsets import ViewSet,ModelViewSet
from api.serializers import PostSerializer,UserSerializer,CommentSerializer
from rest_framework.response import Response
from api.models import Posts,Comments
from rest_framework import authentication,permissions
from rest_framework.decorators import action

# Create your views here.

class PostsView(ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def list(self,request,*args,**kwargs):
        qs=Posts.objects.all()
        serializer=PostSerializer(qs,many=True)
        return Response(data=serializer.data)
    def create(self,request,*args,**kwargs):
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Posts.objects.get(id=id)
        serializer=PostSerializer(qs)
        return Response(data=serializer.data)
    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        ins=Posts.objects.get(id=id)
        serializer=PostSerializer(instance=ins,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Posts.objects.get(id=id)
        qs.delete()
        return Response({'msg':'is deleted'})


class UserView(ViewSet):
    def create(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class PostModelView(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Posts.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        seralizer=PostSerializer(data=request.data,context={'usr':request.user})
        if seralizer.is_valid():
            seralizer.save()
            return Response(data=seralizer.data)

    @action(methods=["GET"],detail=False)
    def my_posts(self,request,*args,**kwargs):
        user=request.user
        qs=user.post.all()
        serializer=PostSerializer(qs,many=True)
        return Response(data=serializer.data)

    @action(methods=["POST"],detail=True)
    def add_comment(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        pst=Posts.objects.get(id=id)
        serializer=CommentSerializer(data=request.data,context={"user":request.user,"post":pst})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)



    @action(methods=["GET"],detail=True)
    def get_comment(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        post=Posts.objects.get(id=id)
        cmnts=post.comments_set.all()
        serializer=CommentSerializer(cmnts,many=True)
        return Response(data=serializer.data)

    @action(methods=["post"],detail=True)
    def add_like(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        pst=Posts.objects.get(id=id)
        usr=request.user
        pst.liked_by.add(usr)
        return Response(data="ok.!")

#localhost:8000/api/v2/posts/{id}/get_likes
    @action(methods=["GET"],detail=True)
    def get_likes(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        pst=Posts.objects.get(id=id)
        cnt=pst.liked_by.all().count()
        return Response(data=cnt)


