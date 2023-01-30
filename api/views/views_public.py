from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import serializers_blog

class blogs(APIView):
    page_size = 10
    
    def get(self, request):
        page = int(request.query_params.get('page'))

        limit_start = (page - 1) * self.page_size
        limit_end = limit_start + self.page_size

        query_set = serializers_blog.models.Blog.objects.order_by("-id")[limit_start:limit_end]
        
        return Response({
            'message': 'Blogs',
            'blogs': serializers_blog.blog_serializer(query_set, many = True).data
        }, status=status.HTTP_200_OK)

class blog(APIView):
    def get(self, request, id):

        query_set = serializers_blog.models.Blog.objects.get(id = id)
        
        return Response({
            'message': 'Blog',
            'blog': serializers_blog.blog_serializer(query_set, many = False).data
        }, status=status.HTTP_200_OK)