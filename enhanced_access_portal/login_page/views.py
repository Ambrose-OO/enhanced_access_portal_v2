
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse
from django.shortcuts import render

from login_page.models import User

@csrf_protect
def login_page_view(request):
    print(type(request)) # django.core.handlers.wsgi.WSGIRequest
    print(request.COOKIES)
    return render(request, 'login_webpage.html')

# https://www.geeksforgeeks.org/python/csrf-token-in-django/
@csrf_protect
def USER_PROMPT_login_attempt(request):
    if request.method == "POST":
        print(request.COOKIES)
        email_login = request.POST.get("email")
        password_login = request.POST.get("password")
        print(request)
        print(email_login)
        print(password_login)

        for user in User.objects.all():
            if email_login == user.emailaddress:
                if password_login == user.password:
                    print("match")
                    request.session["logged_in"] = True
                    request.session["user_type"] = user.user_type
                    request.session["user_id"] = user.id
                    return JsonResponse({"status": "success", "message": f"Received: {email_login}"})
    print("fail")
    return JsonResponse({"status": "fail", "message": "Only POST allowed"}, status=405)

@csrf_protect
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


