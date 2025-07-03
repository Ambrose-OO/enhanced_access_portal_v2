
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from login_page.models import User

def dashboard_view(request):
    template = loader.get_template('login_webpage.html')
    return HttpResponse(template.render())

#Admins
@csrf_exempt
def ADMIN_PROMPT_create_project(request):
    print("empty")

@csrf_exempt
def ADMIN_PROMPT_update_project_name(request):
    # Update all of the entities "project name" as well
    print("empty")

@csrf_exempt
def ADMIN_PROMPT_project_entity_addition(request):
    print("empty")

@csrf_exempt
def ADMIN_PROMPT_project_entity_removal(request):
    print("empty")

#Both admin and user
@csrf_exempt
def USER_ADMIN_PROMPT_create_vm_group(request):
    print("empty")


#Users
@csrf_exempt
def USER_PROMPT_add_vm_to_vm_group(request):
    print("empty")

@csrf_exempt
def USER_PROMPT_add_vm_to_vm_group(request):
    print("empty")

@csrf_exempt
def USER_PROMPT_register_attempt(request):
    print("empty")


