
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse
from django.shortcuts import render, redirect

from login_page.models import User
from login_page.views import login_page_view

@csrf_protect
def dashboard_view(request):
    print("--------------")
    print("User dashboard")
    
    logged_in_status = request.session.get("logged_in")
    print("Logged in?: " + str(logged_in_status))

    if (logged_in_status is not None):
        if (logged_in_status == True):
            return render(request, 'rdashboard_user.html')

    return redirect("/login_page/") # This method will returns the user to the login page

#Both admin and user
@csrf_protect
def USER_ADMIN_PROMPT_logout_attempt(request):
    if request.method == "POST":
        print("--------------")
        print("Logout request")
        logged_in_status = request.session.get("logged_in")
        print("Logged in?: " + str(logged_in_status))

        if (logged_in_status is not None):
            if (logged_in_status == True):
                print("logging out")
                request.session.flush() # Clearing server side session data on the User
                return JsonResponse(
                    {
                        "status": "success", 
                        "message": "Server succeeded to logout of user session"
                    }
                ) # This method will returns the user to the login page

        return JsonResponse(
            {
                "status": "failure", 
                "message": "Server failed to logout of user session"
            }
        )
        

def USER_ADMIN_PROMPT_create_vm_group(request):
    print("empty")

#Users
@csrf_protect
def USER_PROMPT_add_vm_to_vm_group(request):
    print("empty")

@csrf_protect
def USER_PROMPT_add_vm_to_vm_group(request):
    print("empty")

@csrf_protect
def USER_PROMPT_register_attempt(request):
    print("empty")

#Admins
@csrf_protect
def ADMIN_PROMPT_create_project(request):
    print("empty")

@csrf_protect
def ADMIN_PROMPT_update_project_name(request):
    # Update all of the entities "project name" as well
    print("empty")

@csrf_protect
def ADMIN_PROMPT_project_entity_addition(request):
    print("empty")

@csrf_protect
def ADMIN_PROMPT_project_entity_removal(request):
    print("empty")







