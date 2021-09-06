from django.urls import path
from django.shortcuts import render

'''
add the basic functionality of the database to this view.py module
'''
from . import models

#from To_do_app.models import

'''
import timezone from django web framework
'''
from django.utils import timezone

'''
pip3 install requests before importing requests
'''
import requests

'''
this import helps us redirect to a new page with different url from the current page
'''
from django.shortcuts import redirect

from django.http import HttpResponse

def tasklist(request):
    return HttpResponse('To Do List')
