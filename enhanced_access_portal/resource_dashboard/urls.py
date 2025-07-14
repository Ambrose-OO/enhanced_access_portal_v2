
from django.urls import include, path
from . import views

urlpatterns = [
    path('resource_dashboard/', views.dashboard_view, name='resource_dashboard'),
    path('logout_request/', views.USER_ADMIN_PROMPT_logout_attempt, name="logout_request"),
    path('project_list_request/', views.USER_ADMIN_PROMPT_project_listings, name="project_list_request"),
    path('create_project_request/', views.ADMIN_PROMPT_create_project, name="create_project_request"),
    path('email_name_request/', views.USER_ADMIN_PROMPT_email_name, name="email_name_request")
]