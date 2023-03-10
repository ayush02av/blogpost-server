from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from database import models

class user_serializer(serializers.ModelSerializer):
	class Meta:
		model = models.User
		fields = (
			'id',
			'username',
			'email'
		)

class signup_user_serializer(serializers.ModelSerializer):
	email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset = models.User.objects.all())])

	password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
	password2 = serializers.CharField(write_only=True, required=True)

	class Meta:
		model = models.User
		fields = (
			'username',
			'password',
			'password2',
			'email',
			'first_name',
			'last_name'
		)
		extra_kwargs = {
			'first_name': {'required': True},
			'last_name': {'required': True}
		}

	def validate(self, attrs):
		if attrs['password'] != attrs['password2']:
			raise serializers.ValidationError({"password": "Password fields didn't match."})

		return attrs

	def create(self, validated_data):
		instance = models.User.objects.create(
			username = validated_data['username'],
			email = validated_data['email'],
			first_name = validated_data['first_name'],
			last_name = validated_data['last_name']
		)

		instance.set_password(validated_data['password'])
		instance.save()

		return instance

class login_user_serializer(serializers.ModelSerializer):
	class Meta:
		model = models.User
		fields = ('username', 'password')
		extra_kwargs = {
            'password': {'write_only': True}
        }

class user_reset_password_serializer(serializers.Serializer):
	old_password = serializers.CharField(required=True)
	new_password = serializers.CharField(required=True)

	class Meta:
		model = models.User
		fields = ()
		extra_kwargs = {
            'password': {'write_only': True}
        }