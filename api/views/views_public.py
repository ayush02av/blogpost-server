from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import serializers_blog
    
class blogs(APIView):
    def get(self, request):
        return Response({
            'message': 'Blogs',
            'user': serializers_blog.blog_serializer(serializers_blog.models.Blog.objects.all(), many = True).data
        }, status=status.HTTP_200_OK)