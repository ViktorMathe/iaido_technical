from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Person


class UserRegistration(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({"Error": "Password Does not match"})

        if User.objects.filter(username = self.validated_data['username']).exists():
            raise serializers.ValidationError({"Error": "Username already used"})

        user = User(username=self.validated_data['username'])
        user.set_password(password)
        user.save()

        return user

class PersonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('first_name', 'last_name','email', 'phone_number', 'date_of_birth','age')

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('first_name', 'last_name','email', 'phone_number', 'date_of_birth','age', 'username', 'password')