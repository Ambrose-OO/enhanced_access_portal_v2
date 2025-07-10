
from django.urls import include, path
from . import views

urlpatterns = [
    path('resource_dashboard/', views.dashboard_view, name='resource_dashboard'),
    path('logout_request/', views.USER_ADMIN_PROMPT_logout_attempt, name="logout_request"),
    path('project_list_request/', views.USER_ADMIN_PROMPT_logout_attempt, name="project_list_request")
]