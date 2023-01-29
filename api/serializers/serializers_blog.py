from rest_framework import serializers
from database import models
from api.serializers.serializers_user import models, user_serializer

class blog_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = (
            'id',
            'title',
            'content',
            'author',
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['author'] = user_serializer(
            models.User.objects.get(id = response['author']), many = False
        ).data
        
        return response