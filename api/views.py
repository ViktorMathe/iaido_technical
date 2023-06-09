from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UserRegistration, PersonListSerializer, PersonSerializer
from django.contrib.auth import authenticate, login
from .models import Person
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Person List': 'person_list/',
        'Signup': 'signup/',
        'Log In': 'login/',
        'Filter by Last Name': '',
        'Filter by First Name': '',
        'Filter by Age': '',
        'Add a Person (Admin Only)': '/create',
        'Update a Person (Admin Only)': '/update/pk',
        'Delete a Person (Admin Only)': '/person/pk/delete'
    }
 
    return Response(api_urls)


@api_view(["POST"])
def user_signup_view(request):
    if request.method == "POST":
        serializers = UserRegistration(data=request.data)

        data = {}

        if serializers.is_valid():
            user = serializers.save()

            data['response'] = 'User has been created'
            data['username'] = user.username

            token = Token.objects.get(user=user).key
            data['token'] = token
        
        else:
            data = serializers.errors
            
        return Response(data)

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        user.is_active==True
        return Response({'message': 'Login successful'})
        request.session.save()
    else:
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsSuperUser])
def create_person(request, format=None):
    person = PersonSerializer(data=request.data)

    if Person.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
    
    if person.is_valid():
         person.user = User
         person.save()
         return Response(person.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET','POST'])
@permission_classes([IsSuperUser])
def update_person(request, pk):
    person = Person.objects.get(pk=pk)
    data = PersonSerializer(instance=person, data=request.data)
 
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsSuperUser])
def delete_person(request, pk):
    person = get_object_or_404(Person, pk=pk)
    person.delete()
    return Response(status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def person_list(request):
    if request.query_params:
        persons = Person.objects.filter(**request.query_params.dict())
    else:
        persons = Person.objects.all()
 
    if persons:
        serializer = PersonListSerializer(persons, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
