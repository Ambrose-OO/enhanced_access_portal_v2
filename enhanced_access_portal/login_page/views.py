
from django.http import HttpResponse
from django.template import loader

def login_page_view(request):
    template = loader.get_template('login_webpage.html')
    return HttpResponse(template.render())