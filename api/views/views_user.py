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

class blogs(APIView):
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
        data = request.data
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

class blog(APIView):
    serializer_class = serializers_blog.blog_serializer
    blog = None
    
    def __blog_validate__(self, request, pk):
        try:
            blog = serializers_blog.models.Blog.objects.get(id = pk)

            if blog.author != request.user:
                return Response({
                    'message': 'Blog access forbidden'
                }, status=status.HTTP_403_FORBIDDEN)
            
        except Exception as exception:
            return Response({
                'message': exception.__str__()
            }, status=status.HTTP_404_NOT_FOUND)
        
        self.blog = blog
        return True
    
    def get(self, request, pk):
        blog = self.__blog_validate__(request, pk)
        if blog != True:
            return blog
        
        return Response({
            'message': 'User blog',
            'blog': self.serializer_class(self.blog).data
        }, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        blog = self.__blog_validate__(request, pk)
        if blog != True:
            return blog
        
        data = request.data
        data['id'] = self.blog.id
        data['author'] = request.user.id

        serializer = self.serializer_class(self.blog, data = data)

        if(serializer.is_valid()):
            serializer.save()
            return Response({
                'message': 'Blog updated',
                'blog': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': 'Blog could not be updated',
                'errors': serializer.errors.__dict__()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, pk):
        blog = self.__blog_validate__(request, pk)
        if blog != True:
            return blog
        
        self.blog.delete()
        
        return Response({
            'message': 'Blog deleted'
        }, status=status.HTTP_204_NO_CONTENT)