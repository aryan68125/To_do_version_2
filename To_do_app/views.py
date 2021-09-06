from django.shortcuts import render

'''
for to create view we need to import
UpdateView is pretty similar to createView and its gonna be imported from django.views.generic.edit
'''
from django.views.generic.edit import CreateView , UpdateView

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

'''import reverse_lazy and it will redirect our user to a certain parts of our page or application'''
from django.urls import reverse_lazy

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

'''
createView has more complex logic because we are actually sending a post request to create an item
by default the CreateView is gonna look for task_form.html
'''
class TaskCreate(CreateView):
     model = Task

     '''
     by default the CreateView uses model form to work with
     it's basically a class represntation of a Form based on a model so it's gonna take the Task Model from models.py of our application in the
     django project and create all the fields by default

     here we wanna list out all of the fields in our from so
     fields = '__all__' will list out all of the items in the field
     '''
     fields = '__all__'

     '''
     so I also wann make sure that we can redirect the user successfully to a different page so we also need to add this to our
     createView

     so in here we need to set the attribute of sucess_url
     if everything goes correctly then go ahead and redirect user to 'task'
     when we create an item just send that user back to the list
     '''
     success_url = reverse_lazy('tasks')

'''
this UpdateView is supposed to take in an item and its supposed to prefill an form
and once we submit it is supposed to modify the data in the database
bydefault this UpdateView will look for the template named model_name_form.html here in my case it will look for
task_form.html
'''
class TaskUpdate(UpdateView):
    model = Task

    '''
    by default the CreateView uses model form to work with
    it's basically a class represntation of a Form based on a model so it's gonna take the Task Model from models.py of our application in the
    django project and create all the fields by default

    here we wanna list out all of the fields in our from so
    fields = '__all__' will list out all of the items in the field
    '''
    fields = '__all__'

    '''
    so I also wann make sure that we can redirect the user successfully to a different page so we also need to add this to our
    createView

    so in here we need to set the attribute of sucess_url
    if everything goes correctly then go ahead and redirect user to 'task'
    when we create an item just send that user back to the list
    '''
    success_url = reverse_lazy('tasks')
