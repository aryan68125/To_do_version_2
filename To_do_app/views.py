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

'''import the class Task inside the models.py file of your application in django project'''
from . models import Task

'''
here in this views.py file for our app we are gonna use class based views
'''
from django.views.generic.list import ListView

'''
create a class named TaskList and inherit the ListView
and this ListView is supposed to return back a template with a query set of data

bydefault class ListView looks for the template named yourAppName_list.html
so we need to change that and configure the class to use our custome template here in my case it is index.html

so the class TaskList has inherited all the functionality of a ListView parent class
ListView parent class will search the template named task_list.html in the directory
To_do(project_name)/To_do_app(app_name)/templates/To_do_app(folder name)/task_list.html
note you should create the file in this directory only otherwise the django project will crash
'''
class TaskList(ListView):
    model = Task
    '''
    now we want to pass the data onto our template (frontend)
    so how do wwe get that query set onto our template , how do we go pass it in

    Bydefault django calls that query set objectList
    django is gonna look for objects_list which is the default name  of the context_object_name

    so inorder to give the context_object_name (objects_list by default) your own name
    just type context_object_name = 'tasks'
    and now in pur template we can refer to our context_object_name as tasks
    '''
    context_object_name = 'tasks'
