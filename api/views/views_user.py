from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import serializers_user
    
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