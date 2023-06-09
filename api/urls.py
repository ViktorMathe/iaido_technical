from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('', views.api_overview, name='home'),
    path('signup/', views.user_signup_view, name='signup'),
    path('login/',views.login_view, name='login'),
    path('create/', views.create_person, name='create_person'),
    path('update/<int:pk>/', views.update_person, name='update_person'),
    path('person/<int:pk>/delete/', views.delete_person, name='delete_person'),
    path('person_list/', views.person_list, name='person_list'),
]