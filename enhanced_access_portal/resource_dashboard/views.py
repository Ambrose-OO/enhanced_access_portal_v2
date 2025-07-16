
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse
from django.shortcuts import render, redirect

from login_page.models import User
from login_page.views import login_page_view

from resource_dashboard.models import Projects
from resource_dashboard.models import VMs


#Both admin and user
def fetch_user_from_id(user_id: int):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None
    
def fetch_project_from_id(project_id: int):
    try:
        return Projects.objects.get(id=project_id)
    except Projects.DoesNotExist:
        return None
    
def fetch_vm_from_id(vm_id: int):
    try:
        return VMs.objects.get(id=vm_id)
    except Projects.DoesNotExist:
        return None

    
def insert_data():
    # Function used to add in VM data
    print("Inserting data")
    vm_logs = [
        ["Mechanical Simulation", "Online", "123.0.255.1", 1, None],
        ["C++ development", "Offline", "56.126.34.2", 1, None],
        ["Python development", "Offline", "255.123.0.1", 1, None],
        ["Hosting machine", "Offline", "233.123.255.3", 1, None],
        ["C development", "Online", "233.255.56.2", 1, None],
        ["Web development", "Online", "135.0.255.1", 1, None],
        ["General Modelling & Simulation", "Online", "137.123.6.1", 1, None],
        ["Ambroses Development VM", "Online", "255.56.7.1", 1, None],
        ["Conans Development VM", "Offline", "41.123.23.1", 1, None],
        ["Jacobs Development VM", "Online", "214.255.123.3", 1, None]
    ]

    for log in vm_logs:
        vm = VMs(
            vm_name = log[0],
            vm_online = log[1],
            vm_ip = log[2],
            owner_id = fetch_user_from_id(log[3])
        )
        vm.save()

@csrf_protect
def dashboard_view(request):
    print("--------------")
    print("User dashboard")
     
    logged_in_status = request.session.get("logged_in")
    user_type = request.session.get("user_type")
    print("Logged in?: " + str(logged_in_status))

    #insert_data()

    if (logged_in_status is not None) and (user_type is not None):
        if (logged_in_status == True):
            if (user_type == "USER"):
                return render(request, 'rdashboard_user.html')
            elif (user_type == "ADMIN"):
                return render(request, 'rdashboard_admin.html')

    return redirect("/login_page/") # This method will returns the user to the login page



def fetch_project_details(project: Projects):
    project_detail = {}

    # Fetch project name
    project_detail["project_name"] = project.project_name
    
    # Fetch project id
    project_detail["project_id"] = project.id
    
    # Fetch project identifier code
    project_detail["project_identifier_code"] = project.project_identifier_code

    # Fetch project owner name
    for user in User.objects.all():
        if (user.id == project.owner_id):
            project_detail["project_owner"] = user.emailaddress
            break

    # Fetch VMs
    available_vms = 0
    vms_online = 0
    project_vms_details = []

    for vm in VMs.objects.all():
        if (vm.project_id == project):
            available_vms += 1
            if vm.vm_online == "online":
                vms_online += 1

            vm_detail = {}
            vm_detail["vm_name"] = vm.vm_name
            vm_detail["vm_status"] = vm.vm_online
            vm_detail["vm_ip"] = vm.vm_ip
            vm_detail["vm_id"] = vm.id

            project_vms_details.append(vm_detail)
    
    project_detail["project_available_vms"] = available_vms
    project_detail["project_vms_online"] = vms_online

    # Fetch project users
    project_users = 0
    project_admins = 0 
    project_member_details = []

    for project2 in Projects.objects.all():
        # Checking if is the same project we are fetching details
        if (project2.id == project.id):
            # Checking if the found project2 is part of project
            # If so, count the user/admin

            if (project2.entity_type) == "ADMIN":
                print("admin fetch")
                project_admins += 1
                
                member_user = fetch_user_from_id(project2.entity_id)

                member_detail = {}
                member_detail["firstname"] = member_user.firstname
                member_detail["emailaddress"] = member_user.emailaddress
                member_detail["type"] = member_user.user_type

                project_member_details.append(member_detail)
                
            if (project2.entity_type) == "USER":
                print("user fetch")
                project_users += 1

                member_user = fetch_user_from_id(project2.entity_id)

                member_detail = {}
                member_detail["firstname"] = member_user.firstname
                member_detail["emailaddress"] = member_user.emailaddress
                member_detail["type"] = member_user.user_type

                project_member_details.append(member_detail)

    project_detail["project_users"] = project_users
    project_detail["project_admins"] = project_admins
    project_detail["project_member_details"] = project_member_details
    project_detail["project_vms_details"] = project_vms_details

    return project_detail


def collate_ADMIN_project_listings():
    admin_project_listings = []

    for project in Projects.objects.all():
        project_detail = {}

        # Admins don't have to be part of a project to see it. They can see all
        project_detail = fetch_project_details(project)    
        admin_project_listings.append(project_detail)
    
    return admin_project_listings

@csrf_protect
def ADMIN_PROMPT_add_vm(request):
    if request.method == "POST":
        print("----------------")
        print("Add vm")

        logged_in_status = request.session.get("logged_in")
        user_type = request.session.get("user_type")

        if (logged_in_status == True):
            if (user_type == "ADMIN"):

                vm_id = request.POST.get("vm_id")
                project_id = request.POST.get("project_id")
                print("b")
                print(vm_id)
                print(project_id)
                vm = fetch_vm_from_id(vm_id)
                project = fetch_project_from_id(project_id)
                print("c")

                if (vm != None) and (project != None):
                    if (vm.project_id == None):
                        print("vm available to add")

                        # Updating vm SQL data to match the given project
                        # https://www.w3schools.com/django/django_update_data.php

                        vm.project_id = project
                        vm.save()
                        
                        admin_project_listings = collate_ADMIN_project_listings()

                        return JsonResponse(
                            {
                                "status": "success", 
                                "message": "Server successfully added vm to project",
                                "projects": admin_project_listings
                            }
                        ) 
                            
                    else:
                        print("vm unavailable to add - error")
                else:
                    print("vm/project can't be found - error")

                return JsonResponse(
                    {
                        "status": "error", 
                        "message": "Server cannot add vm to the project"
                    }
                ) 

        # Failure response if the user is requesting data when logged out
        return JsonResponse(
            {
                "status": "failure", 
                "message": "Server can't pass data on user who is logged out"
            }
        ) 

@csrf_protect
def USER_ADMIN_PROMPT_project_listings(request):
    if request.method == "POST":
        print("----------------")
        print("Project listings")

        logged_in_status = request.session.get("logged_in")
        user_type = request.session.get("user_type")
        user_id = request.session.get("user_id")  

        if (logged_in_status == True):
            if (user_type == "USER"):
                # Variable to store data on projects that the user is allowed to see
                user_project_listings = []

                for project in Projects.objects.all():
                    project_detail = {}

                    # If the user is part of a project then list the project details
                    # to the user
                    if (project.entity_type == "USER"):
                        if (project.entity_id == user_id):
                            project_detail = fetch_project_details(project)    
                            user_project_listings.append(project_detail)

                # Returning project data in JSON format back to the user
                return JsonResponse(
                    {
                        "status": "success", 
                        "message": "Server succeeded pass data on project listings",
                        "projects": user_project_listings
                    }
                ) 
            elif (user_type == "ADMIN"):

                # Variable to store all data on projects for the admin to see
                admin_project_listings = collate_ADMIN_project_listings()

                # Returning project data in JSON format back to the user
                return JsonResponse(
                    {
                        "status": "success", 
                        "message": "Server succeeded pass data on project listings",
                        "projects": admin_project_listings
                    }
                ) 
        
        # Failure response if the user is requesting data when logged out
        return JsonResponse(
            {
                "status": "failure", 
                "message": "Server can't pass data on user who is logged out"
            }
        ) 
    
@csrf_protect
def ADMIN_PROMPT_available_vms(request):
    if request.method == "POST":
        print("---------------------")
        print("Available project VMS")

        logged_in_status = request.session.get("logged_in")
        user_type = request.session.get("user_type")
        user_id = request.session.get("user_id")  

        if (logged_in_status == True):
            if (user_type == "ADMIN"):
                
                available_vms = []

                for vm in VMs.objects.all():
                    if (vm.project_id == None):
                        vm_detail = {}

                        vm_detail["vm_id"] = vm.id
                        vm_detail["vm_name"] = vm.vm_name
                        vm_detail["vm_status"] = vm.vm_online
                        vm_detail["vm_ip"] = vm.vm_ip 
                        available_vms.append(vm_detail) 

                # Returning project data in JSON format back to the user
                return JsonResponse(
                    {
                        "status": "success", 
                        "message": "Server succeeded pass data on project listings",
                        "vms": available_vms
                    }
                ) 
            elif (user_type == "ADMIN"):

                # Variable to store all data on projects for the admin to see
                admin_project_listings = []

                for project in Projects.objects.all():
                    project_detail = {}

                    # Admins don't have to be part of a project to see it. They can see all
                    project_detail = fetch_project_details(project)    
                    admin_project_listings.append(project_detail)

                # Returning project data in JSON format back to the user
                return JsonResponse(
                    {
                        "status": "success", 
                        "message": "Server succeeded pass data on project listings",
                        "projects": admin_project_listings
                    }
                ) 
        
        # Failure response if the user is requesting data when logged out
        return JsonResponse(
            {
                "status": "failure", 
                "message": "Server can't pass data on user who is logged out"
            }
        ) 
    

@csrf_protect
def USER_ADMIN_PROMPT_email_name(request):
    if request.method == "POST":
        print("----------------------")
        print("Email and name display")

        logged_in_status = request.session.get("logged_in")
        user_id = request.session.get("user_id")  

        if (logged_in_status == True):
            
            user = fetch_user_from_id(user_id)
            user_email = user.emailaddress
            user_display_name = user.firstname + ", " + user.lastname

            # Returning project data in JSON format back to the user
            return JsonResponse(
                {
                    "status": "success", 
                    "message": "Server succeeded pass data on project listings",
                    "email": user_email,
                    "name": user_display_name
                }
            ) 
            
        # Failure response if the user is requesting data when logged out
        return JsonResponse(
            {
                "status": "failure", 
                "message": "Server can't pass data on user/admin"
            }
        ) 


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
    if request.method == "POST":

        logged_in_status = request.session.get("logged_in")
        
        if (logged_in_status == True):

            user_type = request.session.get("user_type")
            user_id = request.session.get("user_id")  

            project_name_value = request.POST.get("project_name")
            project_identifier = request.POST.get("project_identifier")

            project = Projects(
                entity_type = user_type,
                entity_id = user_id,
                owner_id_id = user_id,
                project_name = project_name_value,
                project_identifier_code = project_identifier
            )

            project.save()

            return JsonResponse({"status": "success", "message": "Project registered"})
    
    return JsonResponse({"status": "fail", "message": "Only POST allowed"}, status=405)

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







