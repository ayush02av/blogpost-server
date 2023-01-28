from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import serializers_user, serializers_blog
    
class profile(APIView):
    def get(self, request):
        return Response({
            'message': 'User profile',
            'user': serializers_user.user_serializer(request.user, many = False).data
        }, status=status.HTTP_200_OK)

class logout_user(APIView):
    def post(self, request):
        response = Response({
                'message': 'User logged out'
            }, status=status.HTTP_200_OK)
        response.delete_cookie('token')

        return response

class blog(APIView):
    serializer_class = serializers_blog.blog_serializer
    
    def get(self, request):
        return Response({
            'message': 'User blogs',
            'blogs': self.serializer_class(
                serializers_blog.models.Blog.objects.filter(author = request.user),
                many = True
            ).data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.dict()
        data['author'] = request.user.id
        
        serializer = self.serializer_class(data = data)
        
        if(serializer.is_valid()):
            serializer.save()
            return Response({
                'message': 'New blog created',
                'blog': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': 'Blog could not be created',
                'errors': serializer.errors.__dict__()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)