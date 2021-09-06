from django.shortcuts import render

#from To_do_app.models import

'''import the class Task inside the models.py file of your application in django project'''
from . models import Task

'''
here in this views.py file for our app we are gonna use class based views
'''
from django.views.generic.list import ListView

'''
here in this views.py file for our app we are gonna use class based views
'''
from django.views.generic.detail import DetailView

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

'''
this class TaskDetail will inherit all the properties of the DetailView parent class from the inbuilt django classes

this DetailView is gonna look for a template with a prefix of a model_name_detail.html
here in my case its gonna look for task_detail.html and try to return it
import his view class into your apps urls.py file

To customize this name object to anything that we want context_object_name = 'task'

now setting a cutom template name
changing the default template name from task_detail.html to task.html can be achieved by the code below
template_name = 'app_name/task.html' so basically we are telling django to look for task.html instead of task_detail.html
'''
class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'To_do_app/task.html'
