
from django.urls import include, path
from . import views

urlpatterns = [
    path('login_page/', views.login_page_view, name='login_page_view'),
]