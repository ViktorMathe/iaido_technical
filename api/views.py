from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework.authtoken.models import Token
from .serializers import UserRegistration, PersonListSerializer, PersonSerializer
from django.contrib.auth import authenticate, login, logout
from .models import Person
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Person List': 'person_list/',
        'Signup': 'signup/',
        'Log In': 'login/',
        'Filter by First Name': 'person_list/?first_name=<value>',
        'Filter by Last Name': 'person_list/?last_name=<value>',
        'Filter by Age': 'person_list/?age=<value>',
        'CRUD (Admin Only)': 'crud/',
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


class PersonPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PersonCrudView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsSuperUser]
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    pagination_class = PersonPagination
    

class PersonListView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Person.objects.all()
    serializer_class = PersonListSerializer


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
