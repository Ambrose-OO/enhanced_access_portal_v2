
from django.urls import include, path
from . import views

urlpatterns = [
    path('login_page/', views.login_page_view, name='login_page_view'),
    path('', views.login_page_view, name='login_page_view'),
    path('login_request/', views.USER_PROMPT_login_attempt, name="login_request"),
    path('register_request/', views.USER_PROMPT_register_attempt, name="register_request")
]