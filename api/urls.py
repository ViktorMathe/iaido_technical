from django.urls import path, include
from rest_framework import routers
from . import views
from api.views import PersonCrudView, PersonListView
router = routers.DefaultRouter()
router.register(r'persons/crud', PersonCrudView),
router.register(r'persons', PersonListView),

urlpatterns = [
    path('', views.api_overview, name='home'),
    path('', include(router.urls)),
    path('signup/', views.user_signup_view, name='signup'),
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout, name='logout'),
    path('person_list/', views.person_list, name='person_list'),
]