from django.shortcuts import render
from .models import MoviesLikes,Movies,Playlists
from .serializers import MovieSerializer,PlayListSerializer
from auth_modules.models import UserFollowing
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView,CreateAPIView
from rest_framework.permissions import IsAuthenticated


class UploadMovieView(CreateAPIView):
    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        user = self.request.user
        if user.is_uploader:
            return Response({"message":"Upload your Movie"},status = status.HTTP_200_OK)
        else:
            return Response({"message":"Not Authorized"},status=status.HTTP_401_UNAUTHORIZED)
        
    def perform_create(self, serializer):
        serializer.save(uploaded_by = self.request.user)

class MovieLikeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        id = self.request.query_params.get('id')
        movie = Movies.objects.get(id = id)
        try:
          like = MoviesLikes.objects.get(liked_on= movie,liked_by = self.request.user)
          like.delete()
        except:
          MoviesLikes.objects.create(liked_on = movie,liked_by = self.request.user)
        return Response({"Message":"Succesfull"})
  
class CreatePlayListView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PlayListSerializer

    def perform_create(self,serializer):
        serializer.save(owner = self.request.user)

class ViewPlayListView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PlayListSerializer

    def get(self,request,*args, **kwargs):
        id = self.request.query_params.get('id')
        playlist = Playlists.objects.get(id = id)
        if playlist.owner == self.request.user:
            serializer = PlayListSerializer(playlist)
            return Response({"data":serializer.data},status=status.HTTP_200_OK)
        if playlist.is_private:
            user = self.request.user
            owner = playlist.owner
            try:
               followed = UserFollowing.objects.get(user_id = user,following_user_id = owner)
               serializer = PlayListSerializer(playlist)
               return Response({"data":serializer.data},status=status.HTTP_200_OK)
            except:
                return Response({"message":"This Playlist is Private"},status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = PlayListSerializer(playlist)
            return Response({"data":serializer.data},status=status.HTTP_200_OK)