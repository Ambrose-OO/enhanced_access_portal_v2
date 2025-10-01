
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse
from django.shortcuts import render

from login_page.models import User

import re

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


def empty_or_whitespace_string_check(string: str):
    filtered_string = string.strip()
    if (filtered_string != ""):
        for character in filtered_string:
            print("'" + character + "'")
            if (character == "") or (character == " "): 
                return True
        return False
    else:
        return True

def normal_entry_match(string: str):
   # Check for letters (A–Z, a–z), hyphen (-), or apostrophe (')
    return bool(re.fullmatch(r"[A-Za-z'-]+", string))

def valid_email(email: str):
    # Matching for a email format that follows name@domain.tld
    return bool(re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email))

@csrf_protect
def USER_PROMPT_register_attempt(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        other_names = request.POST.get("other_names")

        email_address = request.POST.get("email_address")
        password = request.POST.get("password")
        password_repeat = request.POST.get("password_repeat")

        # Checking for whitespace
        if (empty_or_whitespace_string_check(first_name) == True):
            return JsonResponse(
                {
                    "status": "fail", 
                    "header_message": "Error: First name entry",
                    "message": "Issue with first name entry. No name was entered or it includes whitespace. Please try again."
                }
            )
        elif (empty_or_whitespace_string_check(other_names) == True):
            return JsonResponse(
                {
                    "status": "fail", 
                    "header_message": "Error: Other name entry",
                    "message": "Issue with other names entry. No name was entered or it includes whitespace. Please try again."
                }
            )
        elif (empty_or_whitespace_string_check(email_address) == True):
            return JsonResponse(
                {
                    "status": "fail", 
                    "header_message": "Error: Email entry",
                    "message": "Issue with email entry. No email was entered or it includes whitespace. Please try again."
                }
            )
        elif (empty_or_whitespace_string_check(password) == True):
            return JsonResponse(
                {
                    "status": "fail", 
                    "header_message": "Error: Password entry",
                    "message": "Issue with password entry. No password was entered or it includes whitespace. Please try again."
                }
            )
        elif (empty_or_whitespace_string_check(password_repeat) == True):
            return JsonResponse(
                {
                    "status": "fail", 
                    "header_message": "Error: Repeated password entry",
                    "message": "Issue with repeated password entry. No password was entered or it includes whitespace. Please try again."
                }
            )
        
        # Checking for special characters
        if (normal_entry_match(first_name) == False):
            return JsonResponse(
                {
                    "status": "fail", 
                    "header_message": "Error: First name special characters",
                    "message": "Issue with first name entry. Special characters detected. Remove them, then please try again."
                }
            )
        elif (normal_entry_match(other_names) == False):
            return JsonResponse(
                {
                    "status": "fail", 
                    "header_message": "Error: Other name special characters",
                    "message": "Issue with other names entry. Special characters detected. Remove them, then please try again."
                }
            )
        
        # Checking for length
        if (len(first_name) > 50):
            return JsonResponse(
                {
                    "status": "fail", 
                    "header_message": "Error: First name length",
                    "message": "Issue with first name entry. The length of the first name is too long. Shorten it, then please try again."
                }
            )
        elif (len(other_names) > 70):
            return JsonResponse(
                {
                    "status": "fail", 
                    "header_message": "Error: Other name length",
                    "message": "Issue with other name entry. The length of the other names is too long. Shorten it, then please try again."
                }
            )
        elif (len(email_address) > 50):
            return JsonResponse(
                {
                    "status": "fail", 
                    "header_message": "Error: Email length",
                    "message": "Issue with email entry. The length of the email is too long. Please try again with a shorter more legitmate email."
                }
            )
        elif (len(password) > 50):
            return JsonResponse(
                {
                    "status": "fail", 
                    "header_message": "Error: Password length",
                    "message": "Issue with password entry. The password is too long. Please shorten it and then try again."
                }
            )
        elif (len(password_repeat) != len(password)):
            return JsonResponse(
                {
                    "status": "fail", 
                    "header_message": "Error: Repeated password length",
                    "message": "Issue with repeated password entry. It does not match the length of the repeated password. Re-check the length then please try again."
                }
            )
        
        # Checking email format
        if (valid_email(email_address) == False):
            return JsonResponse(
                {
                    "status": "fail", 
                    "header_message": "Error: Invalid email address format",
                    "message": "Issue with email entry. It follows an incorrect email address format. Enter one of 'name@domain.tld'. Please try again."
                }
            )

        # Checking if the repeated password equates to the original password entry
        if (password_repeat != password):
            return JsonResponse(
                {
                    "status": "fail", 
                    "header_message": "Error: Repeated password match",
                    "message": "Issue with repeated password entry. It does not match the password. Re-check the characters inputted then please try again."
                }
            )
        
        # Final check to see if a email account being registered has been registered already
        for found_user in User.objects.all():
            if (found_user.emailaddress == email_address):
                return JsonResponse(
                {
                    "status": "fail", 
                    "header_message": "Error: Email already exists",
                    "message": "Issue with email entry. As this email is already registered. Input another, then please try again."
                }
            )
    
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


