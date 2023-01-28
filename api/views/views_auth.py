from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from api.serializers import serializers_user
import jwt
from django.conf import settings
from django.contrib.auth import authenticate

def get_authenticated_user_and_token(instance):
    user = serializers_user.user_serializer(serializers_user.models.User.objects.get(username = instance['username']), many=False)
    user = user.data

    token = jwt.encode({
            'id': user['id'],
            'username': user['username'],
            'email': user['email']
        }, settings.JWT_SECRET, algorithm="HS256")

    return {
        'user': user,
        'token': token
    }
    
class signup_user(generics.CreateAPIView):
    queryset = serializers_user.models.User.objects.all()
    serializer_class = serializers_user.signup_user_serializer
    
    def post(self, request):
        instance = self.create(request)
        
        user_and_token = get_authenticated_user_and_token(instance.data)
        
        response = Response({
                'message': 'New user created',
                'user': user_and_token['user']
            }, status=status.HTTP_201_CREATED)
        response.set_cookie('token', user_and_token['token'])

        return response

class login_user(APIView):
    serializer_class = serializers_user.login_user_serializer
    
    def post(self, request):
        instance = authenticate(username=request.data['username'], password=request.data['password'])
        
        if instance == None:
            return Response({
                'message': 'User authentication failed'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        instance = self.serializer_class(instance, many = False)

        user_and_token = get_authenticated_user_and_token(instance.data)
        
        response = Response({
                'message': 'Logged in user',
                'user': user_and_token['user']
            }, status=status.HTTP_200_OK)

        response.set_cookie('token', user_and_token['token'])

        return response