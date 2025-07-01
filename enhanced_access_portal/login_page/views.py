
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from login_page.models import User

def login_page_view(request):
    template = loader.get_template('login_webpage.html')
    return HttpResponse(template.render())

@csrf_exempt
def USER_PROMPT_login_attempt(request):
    if request.method == "POST":
        user_input = request.POST.get("Output1")
        user_input2 = request.POST.get("Output2")
        print(request)
        print(user_input)
        print(user_input2)
        return JsonResponse({"status": "success", "message": f"Received: {user_input}"})
    return JsonResponse({"status": "fail", "message": "Only POST allowed"}, status=405)

@csrf_exempt
def USER_PROMPT_register_attempt(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        other_names = request.POST.get("other_names")

        email_address = request.POST.get("email_address")
        password = request.POST.get("password")

       
        user = User(
            firstname = first_name, 
            lastname = other_names, 
            emailaddress = email_address, 
            password = password, 
            user_type="USER"
        )
        
        user.save()
        return JsonResponse({"status": "success", "message": "Account registered"})
        #except:
        #     return JsonResponse({"status": "fail", "message": "Registration process failed"})
        
    return JsonResponse({"status": "fail", "message": "Only POST allowed"}, status=405)


