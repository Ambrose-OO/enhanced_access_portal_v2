
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse
from django.shortcuts import render, redirect

from login_page.models import User
from login_page.views import login_page_view

from resource_dashboard.models import Projects
from resource_dashboard.models import VMs
from resource_dashboard.models import VM_Group

###################
# Generic functions
###################

def fetch_user_from_id(user_id: int):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None
    
def fetch_project_from_id(project_id: int):
    try:
        return Projects.objects.get(id=project_id, entity_type="PROJECT")
    except Projects.DoesNotExist:
        return None

def fetch_group_from_id(group_id: int):
    try:
        return VM_Group.objects.get(id=group_id)
    except VM_Group.DoesNotExist:
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
        ["Data Analytics VM", "Online", "192.168.10.21", 1, None],
        ["Machine Learning Node", "Offline", "172.16.34.56", 1, None],
        ["AI Research VM", "Online", "10.45.123.77", 1, None],
        ["Finance Modelling Server", "Offline", "203.0.113.45", 1, None],
        ["HR Payroll Processing", "Online", "198.51.100.23", 1, None],
        ["Testing Environment", "Offline", "192.0.2.111", 1, None],
        ["Cybersecurity Sandbox", "Online", "156.34.78.9", 1, None],
        ["Database Backup Node", "Offline", "145.23.56.200", 1, None],
        ["Frontend Dev VM", "Online", "134.56.77.89", 1, None],
        ["Backend Dev VM", "Online", "165.34.87.101", 1, None],
        ["Linux Kernel Dev VM", "Offline", "176.56.120.33", 1, None],
        ["Windows Build Server", "Online", "143.22.67.89", 1, None],
        ["Cross-platform Testing", "Offline", "154.77.23.45", 1, None],
        ["Networking Simulation Node", "Online", "190.123.67.22", 1, None],
        ["GIS Analysis VM", "Offline", "201.56.89.76", 1, None],
        ["Climate Modelling Server", "Online", "178.200.45.66", 1, None],
        ["Legal Docs Processing", "Offline", "164.90.123.34", 1, None],
        ["Digital Twin Engine", "Online", "177.23.44.55", 1, None],
        ["Quantum Simulation Node", "Offline", "182.56.100.9", 1, None],
        ["Big Data Processing", "Online", "143.67.210.11", 1, None],
        ["Email Server VM", "Online", "198.12.34.56", 1, None],
        ["Code Review Server", "Offline", "201.45.67.89", 1, None],
        ["Continuous Integration VM", "Online", "172.88.99.44", 1, None],
        ["Automated Testing VM", "Offline", "185.77.66.22", 1, None],
        ["File Storage Node", "Online", "139.45.120.66", 1, None],
        ["Load Balancer VM", "Offline", "204.12.44.78", 1, None],
        ["API Gateway Server", "Online", "156.90.67.23", 1, None],
        ["Blockchain Dev VM", "Offline", "193.120.45.99", 1, None],
        ["Edge Computing Node", "Online", "154.56.200.77", 1, None],
        ["IoT Device Management VM", "Offline", "178.66.99.123", 1, None]
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
            if vm.vm_online == "Online":
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
        if (project2.project_identifier_code == project.project_identifier_code):
            # Checking if the found project2 is part of project
            # If so, count the user/admin

            if (project2.entity_type) == "ADMIN":
                #print("admin fetch")
                project_admins += 1
                
                member_user = fetch_user_from_id(project2.entity_id)

                member_detail = {}
                member_detail["firstname"] = member_user.firstname
                member_detail["emailaddress"] = member_user.emailaddress
                member_detail["type"] = member_user.user_type
                member_detail["user_id"] = member_user.id

                project_member_details.append(member_detail)
                
            if (project2.entity_type) == "USER":
                
                project_users += 1

                member_user = fetch_user_from_id(project2.entity_id)

                member_detail = {}
                member_detail["firstname"] = member_user.firstname
                member_detail["emailaddress"] = member_user.emailaddress
                member_detail["type"] = member_user.user_type
                member_detail["user_id"] = member_user.id

                project_member_details.append(member_detail)

    project_detail["project_users"] = project_users
    project_detail["project_admins"] = project_admins
    project_detail["project_member_details"] = project_member_details
    project_detail["project_vms_details"] = project_vms_details

    project_detail["entity_type"] = project.entity_type

    return project_detail

def fetch_group_details(group: VM_Group):
    group_detail = {}

    # Fetch group details
    group_detail["group_name"] = group.vm_group_name
    group_detail["created_date"] = group.created_date
    group_detail["group_id"] = group.id 

    # Fetch vm details
    group_detail["group_root"] = True
    if (group.vm_id != None):
        vm = group.vm_id
        group_detail["group_root"] = False

        group_detail["vm_name"] = vm.vm_name
        group_detail["vm_status"] = vm.vm_online
        group_detail["vm_ip"] = vm.vm_ip
        group_detail["vm_id"] = vm.id

    return group_detail


def collate_ADMIN_project_listings():
    admin_project_listings = []

    for project in Projects.objects.all():
        project_detail = {}

        # Admins don't have to be part of a project to see it. They can see all
        project_detail = fetch_project_details(project)    
        admin_project_listings.append(project_detail)
    
    return admin_project_listings


####################
#Both admin and user
####################


def fetch_group_listings(user_id):
    # Variable to store data on private groups
    group_metadata = {}
    user_group_listings = []
    user = fetch_user_from_id(user_id)

    for group in VM_Group.objects.all():
        group_detail = {}

        # If the user is part of a project then list the project details
        # to the user
        if (group.owner_id == user):
            if (group.vm_id == None):
                group_metadata["group_name"] = group.vm_group_name
                group_metadata["created_date"] = group.created_date
                group_metadata["group_id"] = group.id 

            group_detail = fetch_group_details(group) 
                
            user_group_listings.append(group_detail)
    
    return [group_metadata, user_group_listings]

# Groups
@csrf_protect
def USER_ADMIN_PROMPT_group_listings(request):
    if request.method == "POST":
        # print("--------------")
        # print("Group listings")

        logged_in_status = request.session.get("logged_in")
        user_id = request.session.get("user_id")  

        if (logged_in_status == True):
            
            # Variable to store data on private groups
            fetch_group_listings_return = fetch_group_listings(user_id)
            group_metadata = fetch_group_listings_return[0]
            user_group_listings = fetch_group_listings_return[1]
            
            # Returning project data in JSON format back to the user
            return JsonResponse(
                {
                    "status": "success", 
                    "message": "Server succeeded pass data on group listings",
                    "groups": {
                        "listings": user_group_listings,
                        "meta_data": group_metadata
                    }
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
def USER_ADMIN_PROMPT_create_vm_group(request):
    if request.method == "POST":

        logged_in_status = request.session.get("logged_in")
        
        if (logged_in_status == True):
            
            group_name = request.POST.get("group_name")

            if (group_name != None):
                
                if (len(group_name) < 3):
                    return JsonResponse(
                        {
                            "status": "fail", 
                            "header_message": "Error: VM group name length",
                            "message": "Issue with creating a VM group. As the group name has less than three characters. Please try again."
                        }
                    )
                
                user_id = request.session.get("user_id")  
                user = fetch_user_from_id(user_id)

                for vm_group in VM_Group.objects.all():
                    if (vm_group.vm_group_name == group_name) and (vm_group.owner_id == user):
                        return JsonResponse(
                            {
                                "status": "fail", 
                                "header_message": "Error: VM group duplicate name",
                                "message": "Issue with creating a VM group. As one already exists with the same name. Please try again"
                            }
                        )
                            
                group_root_entry = VM_Group(
                    owner_id = fetch_user_from_id(user_id),
                    vm_group_name = group_name
                )
                group_root_entry.save()

                # Variable to store data on private groups
                fetch_group_listings_return = fetch_group_listings(user_id)
                group_metadata = fetch_group_listings_return[0]
                user_group_listings = fetch_group_listings_return[1]
                
                return JsonResponse(
                    {
                        "status": "success", 
                        "message": "Group created",
                        "groups": {
                            "listings": user_group_listings,
                            "meta_data": group_metadata
                        }
                    }
                )

    return JsonResponse({"status": "fail", "message": "Only POST allowed"}, status=405)

@csrf_protect
def USER_ADMIN_PROMPT_delete_vm_group(request):
    if request.method == "POST":

        logged_in_status = request.session.get("logged_in")
        
        if (logged_in_status == True):
            
            group_id = request.POST.get("group_id")
            group = fetch_group_from_id(group_id)

            user_id = request.session.get("user_id")  
            user = fetch_user_from_id(user_id)

            if (group):
                # Checking if the person requesting to delete the group
                # actually owns it as an additional security check
                if (group.owner_id == user):
                    
                    # Need to delete Group VM entries associated with the Group entry
                    for found_group in VM_Group.objects.all():
                        if (found_group.owner_id == user) and (found_group.vm_group_name == group.vm_group_name):
                            found_group.delete()
                    
                    group.delete()

                    return JsonResponse(
                        {
                            "status": "success", 
                            "header_message": "Success: Server deleted the group",
                            "message": "Server successfully deleted the project from the database."
                        }
                    ) 
                else:
                    return JsonResponse(
                        {
                            "status": "fail", 
                            "header_message": "Error: You do not own the group you attempted to delete",
                            "message": "There must be an issue with linking your user_id to your session. Please re-log in and try again."
                        }
                    ) 
            else:
                return JsonResponse(
                    {
                        "status": "fail", 
                        "header_message": "Error: Group doesn't exist",
                        "message": "The group you attempted to delete does not exist. Please try selecting a group again for deletion."
                    }
                ) 

                

    return JsonResponse({"status": "fail", "message": "Only POST allowed"}, status=405)

#@csrf_protect
#def USER_ADMIN_PROMPT_add_vm_to_vm_group(request):
#    return

@csrf_protect
def USER_ADMIN_PROMPT_remove_group_vm(request):
    return

def collate_USER_project_listings(user):
    # Variable to store data on projects that the user is allowed to see
    user_project_listings = []
    
    for project in Projects.objects.all():
        project_detail = {}

        # If the user is part of a project then list the project details
        # to the user
        if (project.entity_type == "PROJECT"):
            if (user_exists_in_project(user, project) == True):
                project_detail = fetch_project_details(project)    
                user_project_listings.append(project_detail)

    return

# Project listings
@csrf_protect
def USER_ADMIN_PROMPT_project_listings(request):
    if request.method == "POST":

        debug_id = request.POST.get("debug_id")

        print()
                
        logged_in_status = request.session.get("logged_in")
        user_type = request.session.get("user_type")
        user_id = request.session.get("user_id")  
        user = fetch_user_from_id(user_id)

        print(debug_id + " Server: Point B - Project listings\n")

        if (logged_in_status == True) and (user):
            if (user_type == "USER"):
                print(debug_id + " Server: Point B.1.1-User - Project listings\n")

                # Variable to store data on projects that the user is allowed to see
                user_project_listings = collate_USER_project_listings(user)
                
                print(debug_id + " Server: Point B.1.2-User - Project listings\n")

                # Returning project data in JSON format back to the user
                return JsonResponse(
                    {
                        "status": "success", 
                        "message": "Server succeeded pass data on project listings",
                        "projects": user_project_listings
                    }
                ) 
            elif (user_type == "ADMIN"):

                print(debug_id + " Server: Point B.2.1-Admin - Project listings\n")

                # Variable to store all data on projects for the admin to see
                admin_project_listings = collate_ADMIN_project_listings()

                print(debug_id + " Server: Point B.2.2-Admin - Project listings")

                # Returning project data in JSON format back to the user
                return JsonResponse(
                    {
                        "status": "success", 
                        "message": "Server succeeded pass data on project listings",
                        "projects": admin_project_listings
                    }
                ) 
        else:
            # Failure response if the user is requesting data when logged out
            return JsonResponse(
                {
                    "status": "fail", 
                    "header_message": "Error: Logged out",
                    "message": "Error passing data on project listings as you are logged out. Please log in and try again."
                }
            )

def collate_available_project_vms():

    available_vms = []
    
    for vm in VMs.objects.all():
        if (vm.project_id == None):
            vm_detail = {}

            vm_detail["vm_id"] = vm.id
            vm_detail["vm_name"] = vm.vm_name
            vm_detail["vm_status"] = vm.vm_online
            vm_detail["vm_ip"] = vm.vm_ip 
            available_vms.append(vm_detail) 

    return available_vms

    
@csrf_protect
def USRER_ADMIN_PROMPT_available_vms(request):
    if request.method == "POST":
        # print("---------------------")
        # print("Available project VMS")

        logged_in_status = request.session.get("logged_in")
        

        """
        Removed these two lines; Removed consideration on filtering available VMS based on user type
            user_type = request.session.get("user_type")
            user_id = request.session.get("user_id")  

        Mostly because of the fact that in an organisation seeing the number of available VMS for transparency
        and to spot any issues in available resources as an trusted employee makes sense.
        """
        
        if (logged_in_status == True):
            
            # Returning project data in JSON format back to the user
            return JsonResponse(
                {
                    "status": "success", 
                    "message": "Server succeeded pass data on available vms",
                    "vms": collate_available_project_vms()
                }
            ) 
            
        # Failure response if the user is requesting data when logged out
        return JsonResponse(
            {
                "status": "failure", 
                "header_message": "Error: Error in retrieving data",
                "message": "Server can't pass data on user who is logged out"
            }
        )


@csrf_protect
def USRER_ADMIN_PROMPT_available_vms_for_group(request):
    if request.method == "POST":
        # print("-----------------------")
        # print("Available VMS for group")

        logged_in_status = request.session.get("logged_in")
        user_type = request.session.get("user_type")

        group_name_target = request.POST.get("group_name_target")
       
        if (logged_in_status == True):
            
            available_vms = []
   
            for vm in VMs.objects.all():
                # If the user_type is an ADMIN, they can view all 
                # VMs to add to their own private group

                # Else USER, then one should just check
                # if vm.project_id == NONE to know if the VM is not
                # assigned to a current project
                if (user_type == "ADMIN") or (vm.project_id == None):
                    
                    # Additional filter to see if the VM is not already
                    # in the group to hide it from the list
                    vm_is_not_in_group = True

                    for found_group in VM_Group.objects.all():
                        # Looking at group vm entries
                        if (found_group.vm_id != None):
                            if (found_group.vm_group_name == group_name_target):
                                if (found_group.vm_id == vm):
                                    vm_is_not_in_group = False

                    if (vm_is_not_in_group == True):
                
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
                    "message": "Server succeeded pass data on available vms",
                    "vms": available_vms
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
def USRER_ADMIN_PROMPT_add_vm_to_group(request):
    if request.method == "POST":
        # print("----------------")
        # print("Add vm to group")

        logged_in_status = request.session.get("logged_in")
        
        if (logged_in_status == True):

            vm_id = request.POST.get("vm_id")
            group_name = request.POST.get("group_name")

            group_exists = False
            vm_already_exists = False
            vm = fetch_vm_from_id(vm_id)

            for found_group in VM_Group.objects.all():    
                if (found_group.vm_group_name == group_name):
                    group_exists = True

                    # Since the loop will continue through every other entry for the group,
                    # a check on whether the vm exists in the group can be made 
                    if (found_group.vm_id == vm_id):
                        vm_already_exists == True

            
            if (group_exists) and (vm) and (vm_already_exists == False):
                user_id = request.session.get("user_id")  
            
                group_root_entry = VM_Group(
                    owner_id = fetch_user_from_id(user_id),
                    vm_group_name = group_name,
                    vm_id = vm
                )
                group_root_entry.save()

                fetch_group_listings_return = fetch_group_listings(user_id)
                group_metadata = fetch_group_listings_return[0]
                user_group_listings = fetch_group_listings_return[1]

                # Returning project data in JSON format back to the user
                return JsonResponse(
                    {
                        "status": "success", 
                        "header_message": "Success: Server added vm to the group",
                        "message": "Server succeeded in adding the selected vm to the group.",
                        "groups": {
                            "listings": user_group_listings,
                            "meta_data": group_metadata
                        }
                    }
                ) 
            else:
                if (not group_exists):
                    return JsonResponse(
                        {
                            "status": "fail", 
                            "header_message": "Error: Can't identify selected group",
                            "message": "The selected group to add the vm to does not exist."
                        }
                    )
                elif (not vm):
                    return JsonResponse(
                        {
                            "status": "fail", 
                            "header_message": "Error: Can't identify selected vm",
                            "message": "Selected vm to add to the group cannot be identified."
                        }
                    )
                elif (vm_already_exists == True):
                    return JsonResponse(
                        {
                            "status": "fail", 
                            "header_message": "Error: VM already in the group",
                            "message": "Selected vm to add to the group is already in the group."
                        }
                    )
            
        else:
            
            # Failure response if the user is requesting data when logged out
            return JsonResponse(
                {
                    "status": "fail", 
                    "header_message": "Error: Logged out",
                    "message": "Server can't pass data on user who is logged out."
                }
            )


@csrf_protect
def USRER_ADMIN_PROMPT_statistics(request):
    if request.method == "POST":
        # print("-------------------")
        # print("Statistics request")

        logged_in_status = request.session.get("logged_in")
       
        if (logged_in_status == True):

            # VM Data
            vm_total = 0
            vms_online = 0
            vms_offline = 0

            unassigned_project_vms = 0
            assigned_project_vms = 0 

            for vm in VMs.objects.all():
                vm_total += 1

                if (vm.vm_online == "Online"):
                    vms_online += 1
                else:
                    vms_offline += 1

                if (vm.project_id == None):
                    unassigned_project_vms += 1
                else:
                    assigned_project_vms += 1 
            
            # Version number data
            version_number = "1.0"

            # System users data
            user_total = 0
            admins_total = 0 
            system_users_total = 0

            for user in User.objects.all():
                system_users_total += 1

                if (user.user_type == "ADMIN"):
                    admins_total += 1
                else:
                    user_total += 1

            # Group and project totals data
            project_total = 0
            group_total = 0

            for found_project in Projects.objects.all():
                if (found_project.entity_type == "PROJECT"):
                    project_total +=1 

            for found_group in VM_Group.objects.all():
                if (found_group.vm_id == None):
                    group_total += 1

            # Returning statistics data in JSON format back to the user
            return JsonResponse(
                {
                    "status": "success", 
                    "message": "Server passing statistic data",
                    "statistics": {
                        "vm_total": vm_total,
                        "vms_online": vms_online,
                        "vms_offline": vms_offline,

                        "unassigned_project_vms": unassigned_project_vms,
                        "assigned_project_vms": assigned_project_vms,

                        "version_number": version_number,

                        "user_total": user_total,
                        "admins_total": admins_total,
                        "system_users_total": system_users_total,

                        "project_total": project_total,
                        "group_total": group_total
                    }
                }
            ) 
        
        else:
            # Failure response if the user is requesting data when logged out
            return JsonResponse(
                {
                    "status": "failure", 
                    "message": "Server can't pass data on user who is logged out"
                }
            ) 


@csrf_protect
def USRER_ADMIN_PROMPT_remove_vm_from_group(request):
    if request.method == "POST":
        # print("----------------------")
        # print("Removing vm from group")

        logged_in_status = request.session.get("logged_in")
    
        if (logged_in_status == True):

            vm_id = request.POST.get("vm_id")
            group_name = request.POST.get("group_name")

            # print("found group name")
            # print(group_name)
            # print("vm id")
            # print(vm_id)

            for found_group in VM_Group.objects.all():
                if (found_group.vm_id != None):    
                    identified_group_name: bool = (found_group.vm_group_name == group_name)
                    
                    vm_id_match: bool = (int((found_group.vm_id).id) == int(vm_id))
                    
                    if (identified_group_name) and (vm_id_match):
                        # Removing the vm from the users group
                        found_group.delete()

                        user_id = request.session.get("user_id")  

                        fetch_group_listings_return = fetch_group_listings(user_id)
                        group_metadata = fetch_group_listings_return[0]
                        user_group_listings = fetch_group_listings_return[1]

                        # Returning project data in JSON format back to the user
                        return JsonResponse(
                            {
                                "status": "success", 
                                "header_message": "Success: Server VM removal from group",
                                "message": "Server succeeded in the removing of selected vm from the group.",
                                "groups": {
                                    "listings": user_group_listings,
                                    "meta_data": group_metadata
                                }
                            }
                        ) 
        
            return JsonResponse(
                {
                    "status": "error", 
                    "message": "Server cannot add vm to the group"
                }
            ) 
        else:
            # Failure response if the user is requesting data when logged out
            return JsonResponse(
                {
                    "status": "failure", 
                    "message": "Server can't pass data on user who is logged out"
                }
            ) 
        

# Display name
@csrf_protect
def USER_ADMIN_PROMPT_email_name(request):
    if request.method == "POST":
        # print("----------------------")
        # print("Email and name display")

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
                    "message": "Server succeeded pass data on email and name display",
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

# Logging out
def USER_ADMIN_PROMPT_logout_attempt(request):
    if request.method == "POST":
        # print("--------------")
        # print("Logout request")
        logged_in_status = request.session.get("logged_in")
        # print("Logged in?: " + str(logged_in_status))

        if (logged_in_status is not None):
            if (logged_in_status == True):
                # print("logging out")
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
        

#######
#Admins
#######

# Projects
@csrf_protect
def ADMIN_PROMPT_delete_project(request):
    if request.method == "POST":
        # print("----------------")
        # print("Delete project")

        logged_in_status = request.session.get("logged_in")
        user_type = request.session.get("user_type")

        if (logged_in_status == True):
            if (user_type == "ADMIN"):

                project_id = request.POST.get("project_id")
                project = fetch_project_from_id(project_id)

                if (project != None):
                    # print("attempting to delete project")
                    project.delete()
                
                    # print("deleted project")

                    return JsonResponse(
                        {
                            "status": "success", 
                            "header_message": "Success: Server deleted the project",
                            "message": "Server successfully deleted the project from the database.",
                            "projects": collate_ADMIN_project_listings()
                        }
                    ) 
                     
                else:
                    return JsonResponse(
                        {
                            "status": "fail", 
                            "header_message": "Error: Can't identify project",
                            "message": "Selected project for deletion cannot be identified. Try again or refresh your page."
                        }
                    )

        return JsonResponse(
            {
                "status": "fail", 
                "header_message": "Error: Cannot delete project entry",
                "message": "Project deletion failure. As the user is not logged in."
            }
        )
    

def ADMIN_USER_PROMPT_rename_project(request):
    if request.method == "POST":
        # print("----------------")
        # print("Renaming project")

        logged_in_status = request.session.get("logged_in")
    
        if (logged_in_status == True):

            project_id = request.POST.get("project_id")
            new_project_name = request.POST.get("new_project_name")
            project = fetch_project_from_id(project_id)

            if (new_project_name) and (new_project_name != ""):

                print("POINT A")

                # Checking if the new project name entered doesn't already exist
                for project in Projects.objects.all():
                    
                    if (project.project_name == new_project_name):
                        print("POINT B")
                        return JsonResponse(
                            {
                                "status": "fail", 
                                "header_message": "Error: Project duplicate name",
                                "message": "Issue with renaming the project. As one already exists with the same name. Please enter a different one, rename the project that is clashing, or delete the clashing project before trying again."
                            }
                        )

                print("POINT B")         
                # Attempting to rename the project
                for project in Projects.objects.all():
                    if (project.entity_type == "PROJECT"):
                        print("POINT C " + str(project.id))
                        if (str(project.id) == str(project_id)) and (str(project.entity_id) == str(0)):
                            print("POINT D")

                            project.project_name = new_project_name
                            project.save()

                            user_type = request.session.get("user_type")
                            user_id = request.session.get("user_id")  
                            
                            if (user_type == "USER"):
                                user = fetch_user_from_id(user_id)
                                return JsonResponse(
                                    {
                                        "status": "success", 
                                        "header_message": "Success: Server renamed the project",
                                        "message": "Server successfully updated the project name with the new inputted one within the database.",
                                        "projects": collate_USER_project_listings(user)
                                    }
                                ) 
                            elif (user_type == "ADMIN"):
                                return JsonResponse(
                                    {
                                        "status": "success", 
                                        "header_message": "Success: Server renamed the project",
                                        "message": "Server successfully updated the project name with the new inputted one within the database.",
                                        "projects": collate_ADMIN_project_listings()
                                    }
                                ) 


                return JsonResponse(
                    {
                        "status": "fail", 
                        "header_message": "Error: Can't identify project",
                        "message": "Selected project for renaming cannot be identified. Try again or refresh your page."
                    }
                )

            else:
                return JsonResponse(
                {
                    "status": "fail", 
                    "header_message": "Error: Missing rename entry",
                    "message": "A project name to rename to hasn't been entered. Try again."
                }
            )
      
        else:
            return JsonResponse(
                {
                    "status": "fail", 
                    "header_message": "Error: Cannot rename project entry",
                    "message": "Project rename failure. As the user is not logged in."
                }
            )


def ADMIN_USER_PROMPT_all_vms(request):
    if request.method == "POST":
        debug_id = request.POST.get("debug_id")

        print()
       
        print(debug_id + " Server: Point B - All vms\n")
        logged_in_status = request.session.get("logged_in")
    
        if (logged_in_status == True):

            print(debug_id + " Server: Point C - All vms\n")

            vms_list = []

            for vm in VMs.objects.all():
                vm_detail = {}

                vm_detail["vm_id"] = vm.id
                vm_detail["vm_name"] = vm.vm_name
                vm_detail["vm_status"] = vm.vm_online
                vm_detail["vm_ip"] = vm.vm_ip 
                vms_list.append(vm_detail) 

            print(debug_id + " Server: Point D - All vms\n")

            return JsonResponse(
                {
                    "status": "success", 
                    "message": "Server succeeded passing data on all vms",
                    "vms": vms_list
                }
            ) 
            
        else:
            return JsonResponse(
                {
                    "status": "fail", 
                    "header_message": "Error: Server error handling the search query",
                    "message": "Cannot pass all vms entries for unknown reason. Please try again."
                }
            )
        
     
def user_exists_in_project(user, project):
    user_in_project = False

    for found_project in Projects.objects.all():
        if (found_project.entity_type == "USER"):

            found_user = fetch_user_from_id(found_project.entity_id)

            # Finding the project entries the user sits in
            if (found_user == user):
                
                if (found_project.project_identifier_code == project.project_identifier_code):
                    user_in_project = True

    return user_in_project

@csrf_protect
def ADMIN_USER_PROMPT_remove_vm(request):
    if request.method == "POST":
        # print("----------------")
        # print("Remove vm")

        logged_in_status = request.session.get("logged_in")
        user_type = request.session.get("user_type")
        user_id = request.session.get("user_id") 
        user = fetch_user_from_id(user_id)

        if (logged_in_status == True) and (user):
            
            vm_id = request.POST.get("vm_id")
            vm = fetch_vm_from_id(vm_id)

            if (vm != None):
                if (vm.project_id != None):
                    
                    if (user_type == "USER"):
                        # Need to check if the user is part of the project that they want
                        # to remove the VM from. As they don't have perms across all projects
                        # like admins do

                        vm_project = vm.project_id
                        user_in_project = user_exists_in_project(user, vm_project)

                        if (user_in_project == False):
                            return JsonResponse(
                                {
                                    "status": "fail", 
                                    "header_message": "Error: Unauthorised request",
                                    "message": "You are not part of the project to be making requests to remove a VM from."
                                }
                            )
                            

                    # Updating vm SQL data to have the VM not be associated with a project
                    # https://www.w3schools.com/django/django_update_data.php
                    vm.project_id = None
                    vm.save()
                    
                    admin_project_listings = collate_ADMIN_project_listings()

                    return JsonResponse(
                        {
                            "status": "success", 
                            "header_message": "Success: Server removed VM from project",
                            "message": "The selected VM for removal has been successfully removed from the project.",
                            "projects": admin_project_listings
                        }
                    )
                        
                else:
                    return JsonResponse(
                        {
                            "status": "fail", 
                            "header_message": "Error: VM is not part of a project",
                            "message": "The selected VM for removal is not part of a project."
                        }
                    )
            else:
                return JsonResponse(
                    {
                        "status": "fail", 
                        "header_message": "Error: VM cannot be identified",
                        "message": "The VM for removal from the project cannot be identified."
                    }
                )

        else:
            # Failure response if the user is requesting data when logged out
            return JsonResponse(
                {
                    "status": "fail", 
                    "header_message": "Error: Logged out",
                    "message": "Error removing VM from project as you are logged out. Please log in and try again."
                }
            )

@csrf_protect
def ADMIN_USER_PROMPT_add_vm(request):
    if request.method == "POST":
        # print("----------------")
        # print("Add vm")

        logged_in_status = request.session.get("logged_in")
        user_type = request.session.get("user_type")
        user_id = request.session.get("user_id") 
        user = fetch_user_from_id(user_id)

        if (logged_in_status == True):
           
            vm_id = request.POST.get("vm_id")
            project_id = request.POST.get("project_id")
            
            vm = fetch_vm_from_id(vm_id)
            project = fetch_project_from_id(project_id)
        
            if (vm != None) and (project != None):
                if (vm.project_id == None):
                    
                    if (user_type == "USER"):
                        # Need to check if the user is part of the project that they want
                        # to add the VM to. As they don't have perms across all projects
                        # like admins do

                        user_in_project = user_exists_in_project(user, project)

                        if (user_in_project == False):
                            return JsonResponse(
                                {
                                    "status": "fail", 
                                    "header_message": "Error: Unauthorised request",
                                    "message": "You are not part of the project to be making requests to add a VM to."
                                }
                            )
                    
                    # Updating vm SQL data to match the given project
                    # https://www.w3schools.com/django/django_update_data.php

                    vm.project_id = project
                    vm.save()
                    
                    admin_project_listings = collate_ADMIN_project_listings()

                    return JsonResponse(
                        {
                            "status": "success", 
                            "header_message": "Success: VM added to project", 
                            "message": "Server successfully added vm to project",
                            "projects": admin_project_listings,
                            "vms": collate_available_project_vms()
                        }
                    ) 
                        
                else:
                    return JsonResponse(
                        {
                            "status": "fail", 
                            "header_message": "Error: VM is part of a project", 
                            "message": "The VM is already part of a project."
                        }
                    )
            else:
                if (vm == None): 
                    return JsonResponse(
                        {
                            "status": "fail", 
                            "header_message": "Error: VM cannot be identified", 
                            "message": "The VM to be added to the project could not be identified."
                        }
                    )
                elif (project == None):
                    return JsonResponse(
                        {
                            "status": "fail", 
                            "header_message": "Error: Project cannot be identified", 
                            "message": "The project for which the selected VM was to be added to cannot be identified."
                        }
                    )
            
        else:

            # Failure response if the user is requesting data when logged out
            return JsonResponse(
                {
                    "status": "fail", 
                    "header_message": "Error: Logged out",
                    "message": "Error adding VM to project as you are logged out. Please log in and try again."
                }
            )


def collate_available_users_given_project(project):
    available_users_details = []
                        
    # Filtering users who are already in the project
    for found_user in User.objects.all():
        user_in_project_of_focus = False

        for found_project in Projects.objects.all():
            
            if (found_project.entity_type == "ADMIN") or (found_project.entity_type == "USER"):
                
                found_project_entity_id = int(found_project.entity_id)
                found_user_id = int(found_user.id)

                if (found_project_entity_id == found_user_id):
                    if (found_project.project_identifier_code == project.project_identifier_code):
                        user_in_project_of_focus = True
    
        if (user_in_project_of_focus == False):
            
            member_detail = {}
            member_detail["firstname"] = found_user.firstname
            member_detail["emailaddress"] = found_user.emailaddress
            member_detail["type"] = found_user.user_type
            member_detail["user_id"] = found_user.id

            available_users_details.append(member_detail)

    return available_users_details


@csrf_protect
def ADMIN_PROMPT_available_users(request):
    if request.method == "POST":
        # print("---------------------")
        # print("Available users")

      
        logged_in_status = request.session.get("logged_in")
        user_type = request.session.get("user_type")
        
        user_id = request.session.get("user_id")  
        user = fetch_user_from_id(user_id)
        
        project_id = int(request.POST.get("project_id"))
        project = fetch_project_from_id(project_id)
        
        if (logged_in_status == True):
    
            if (user != None) and (project != None):
                if (user_type == "ADMIN"):
                    
                    # Returning project data in JSON format back to the user
                    return JsonResponse(
                        {
                            "status": "success", 
                            "message": "Server succeeded passing data on available users",
                            "available_users_details": collate_available_users_given_project(project)
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
def ADMIN_PROMPT_add_user_to_project(request):
    if request.method == "POST":
        # print("---------------------")
        # print("Adding user to project")

        logged_in_status = request.session.get("logged_in")
        user_type = request.session.get("user_type")

        user_id = request.session.get("user_id")  
        user = fetch_user_from_id(user_id)

        user_id_to_add = request.POST.get("user_id")
        user_to_add = fetch_user_from_id(user_id_to_add)

        project_id = request.POST.get("project_id")
        project = fetch_project_from_id(project_id)

        if (logged_in_status == True):
            if (user != None) and (project != None) and (user_to_add != None):
                if (user_type == "ADMIN"):
                    
                    project_entry = Projects(
                        entity_type = user_to_add.user_type,
                        entity_id = user_id_to_add,
                        owner_id = project.owner_id,
                        project_name = project.project_name,
                        project_identifier_code = project.project_identifier_code
                    )

                    project_entry.save()

                    admin_project_listings = collate_ADMIN_project_listings()

                    # Returning project data in JSON format back to the user
                    return JsonResponse(
                        {
                            "status": "success", 
                            "header_message": "Success: Server added user to project",
                            "message": "Server succeeded adding user to project",
                            "projects": admin_project_listings,
                            "available_users_details": collate_available_users_given_project(project)
                        }
                    ) 
                else:
                    return JsonResponse(
                        {
                            "status": "fail", 
                            "header_message": "Error: Unauthorised request",
                            "message": "You are not an admin to be adding users to the project."
                        }
                    )
            else:
                if (user == None):
                    return JsonResponse(
                        {
                            "status": "fail", 
                            "header_message": "Error: Cannot identify your user",
                            "message": "Error identifying your user during the request. Please re-log in and try again."
                        }
                    )
                elif (project == None):
                    return JsonResponse(
                        {
                            "status": "fail", 
                            "header_message": "Error: Project cannot be found",
                            "message": "Project to add the user too cannot be found. Please try again."
                        }
                    )
                elif (user_to_add == None):
                    return JsonResponse(
                        {
                            "status": "fail", 
                            "header_message": "Error: Cannot identify user to add",
                            "message": "Cannot identify the user to add to the project. Please refresh your page and try again."
                        }
                    )
        else:        
            return JsonResponse(
                {
                    "status": "fail", 
                    "header_message": "Error: Logged out",
                    "message": "Error adding user to project as you are logged out. Please log in and try again."
                }
            )
         
    

@csrf_protect
def ADMIN_PROMPT_remove_user_from_project(request):
    if request.method == "POST":
        # print("--------------------------")
        # print("Removing user from project")

        logged_in_status = request.session.get("logged_in")
        user_type = request.session.get("user_type")

        user_id = request.session.get("user_id")  
        user = fetch_user_from_id(user_id)

        user_id_to_remove = int(request.POST.get("user_id"))
        user_to_remove = fetch_user_from_id(user_id_to_remove)

        project_id = request.POST.get("project_id")
        project = fetch_project_from_id(project_id)

        if (logged_in_status == True):
            if (user != None) and (project != None) and (user_to_remove != None):
                if (user_type == "ADMIN"):
                    
                    if (user_to_remove != project.owner_id):
                        # Finding project entries
                        for found_project in Projects.objects.all():
                            
                            found_project_entity_id = int(found_project.entity_id)

                            # Is the project entry a target?
                            if (found_project.project_identifier_code == project.project_identifier_code):
                                # Is it a project entry user type for the target user?
                                if (found_project_entity_id == user_id_to_remove):
                                        found_project.delete()
                                        
                                        admin_project_listings = collate_ADMIN_project_listings()

                                        # Returning project data in JSON format back to the user
                                        return JsonResponse(
                                            {
                                                "status": "success", 
                                                "header_message": "Success: Member removed the project", 
                                                "message": "Server succeeded in deleting the user from the project.",
                                                "projects": admin_project_listings
                                            }
                                        ) 
                        return JsonResponse(
                            {
                                "status": "fail", 
                                "header_message": "Error: Cannot identify project member to remove", 
                                "message": "The server could not find the user you wanted to delete from the project."
                            }
                        )
                    else:
                        return JsonResponse(
                            {
                                "status": "fail", 
                                "header_message": "Error: Cannot remove project owner from the project", 
                                "message": "Cannot remove the project owner from the project. If you wish to do so, go ahead and delete the project if okay."
                            }
                        )
                else:
                    return JsonResponse(
                        {
                            "status": "fail", 
                            "header_message": "Error: Unauthorised request",
                            "message": "You are not an admin to be making requests to remove users from projects."
                        }
                    ) 
            else:
                if (user == None):
                    return JsonResponse(
                        {
                            "status": "fail", 
                            "header_message": "Error: Cannot identify your user",
                            "message": "Error identifying your user during the request. Please re-log in and try again."
                        }
                    )
                elif (project == None):
                    return JsonResponse(
                        {
                            "status": "fail", 
                            "header_message": "Error: Project cannot be found",
                            "message": "Project to remove the project member from cannot be found. Please try again."
                        }
                    )
                elif (user_to_remove == None):
                    return JsonResponse(
                        {
                            "status": "fail", 
                            "header_message": "Error: Cannot identify project member to add",
                            "message": "Cannot identify the member of the project to remove. Please refresh your page and try again."
                        }
                    )

        else:
             return JsonResponse(
                {
                    "status": "fail", 
                    "header_message": "Error: Logged out",
                    "message": "Error removing the memeber from the project as you are logged out. Please log in and try again."
                }
            )
           

@csrf_protect
def ADMIN_PROMPT_create_project(request):
    if request.method == "POST":

        print()

        debug_id = request.POST.get("debug_id")
        print(debug_id + " Server: Point C - Create project attempt")

        logged_in_status = request.session.get("logged_in")
    
        if (logged_in_status == True):

            print(debug_id + " Server: Point D - Create project attempt")

            user_type = request.session.get("user_type")

            if (user_type == "ADMIN"):

                print(debug_id + " Server: Point E.1.1 - Create project attempt")

                user_id = request.session.get("user_id")  

                project_name_value = request.POST.get("project_name")
                project_identifier = request.POST.get("project_identifier")

                if (project_name_value != ""):

                    print(debug_id + " Server: Point E.1.2.A - Create project attempt")

                    if (len(project_name_value) > 2): 

                        print(debug_id + " Server: Point E.1.2.A.1 - Create project attempt")

                        for project in Projects.objects.all():
                            
                            if (project.project_name == project_name_value):
                                print(debug_id + " Server: Point E.1.2.A.2 - Create project attempt")
                                return JsonResponse(
                                    {
                                        "status": "fail", 
                                        "header_message": "Error: Project duplicate name",
                                        "message": "Issue with creating a project. As one already exists with the same name."
                                    }
                                )
                        
                        print(debug_id + " Server: Point E.1.2.A.3 - Create project attempt")
                        project_root_entry = Projects(
                            entity_type = "PROJECT",
                            entity_id = 0, # Can just use the project identifier code to find records for a particulat project then hone in on "PROJECT" entity_type
                            owner_id_id = user_id,
                            project_name = project_name_value,
                            project_identifier_code = project_identifier
                        )
                        project_root_entry.save()

                        print(debug_id + " Server: Point E.1.2.A.4 - Create project attempt")
                        project_admin_entry = Projects(
                            entity_type = user_type,
                            entity_id = user_id,
                            owner_id_id = user_id,
                            project_name = project_name_value,
                            project_identifier_code = project_identifier
                        )
                        project_admin_entry.save()

                        print(debug_id + " Server: Point E.1.2.A.5 - Create project attempt")
                        
                        return JsonResponse(
                            {
                                "status": "success", 
                                "message": "Project registered",
                                "projects": collate_ADMIN_project_listings()
                            })
                    else:
                        print(debug_id + " Server: Point E.1.2.B - Create project attempt")
                        return JsonResponse(
                        {
                            "status": "fail", 
                            "header_message": "Error: Invalid project name",
                            "message": "Project creation failure. Project name has less than 3 characters. Write in at least a 3 character string."
                        }
                    )
                else:
                    print(debug_id + " Server: Point E.2 - Create project attempt")
                    return JsonResponse(
                        {
                            "status": "fail", 
                            "header_message": "Error: Invalid project name",
                            "message": "Project creation failure. Project name has no characters. Write in at least a 3 character string."
                        }
                    )
    
    return JsonResponse({"status": "fail", "message": "Only POST allowed"}, status=405)


