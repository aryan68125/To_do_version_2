from django.shortcuts import render, redirect

'''restrict the user from accessing tasklist if the user is not logged in'''
from django.contrib.auth.mixins import LoginRequiredMixin

'''
for to create view we need to import
UpdateView is pretty similar to createView and its gonna be imported from django.views.generic.edit

FormView allows to generate a from that we will be customizing so that we can use it in our register form View
'''
from django.views.generic.edit import CreateView , UpdateView, DeleteView, FormView

#---------------------------------user registration related imports----------------------------------------------
'''this is a inbuilt django Views class that handles the remdering of views that are built in to the django web framework'''
from django.views.generic import View

'''import messages app that is built in the django web framework'''
from django.contrib import messages

'''install validate-email module before importing it type pip3 install validate-email in your terminal to install the module'''
from validate_email import validate_email

from django.contrib.auth.models import User
'''
construct a url that is unique to the application that we've built so we need the the current domain that our application is running on
and we will set it dynamically we can import this:- from django.contrib.sites.shortcuts import get_current_site
'''
from django.contrib.sites.shortcuts import get_current_site

#now redirect user to the login page
# so inorder to do that you need to import :- from django.template.loader import render_to_string this library renders a template with a context automatically
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from . utils import generated_token
from django.core.mail import EmailMessage
from django.conf import settings
#----------------------------------------------------------------------------------------------------------------------

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
add a loginView into our views.py so that we can use django's inbuilt login page functionality for user login and authentiation of users
in our website
import authentication prebuilt library to authentiacate our users
'''
from django.contrib.auth.views import LoginView




'''
the class below will handel all the functionality of a login page
'''
class CustomLoginView(LoginView):
    '''we don't need model but a template here
       so django already provides us with a login form for our template all we need todo se specify the fields and we are done
    '''
    template_name = 'To_do_app/Login.html'
    fields = '__all__'
    '''
    redirect an authenticated user tham means once the user is authenticated they shouldn't be allowed on this page
    redirect_authenticated_user = False (By default) set redirect_authenticated_user = True
    '''
    redirect_authenticated_user = True

    '''
    override the success url here so once we login in this we will just set a function
    '''
    def get_success_url(self):
        '''send the user to the tasks list page'''
        return reverse_lazy('tasks')

'''
here we will create a registration process for users
use CreateView instaed of FormsView if you want your custom registration field to get render out in register.html
'''
class RegistrationView(View):
    #to handle the get request
    def get(self, request):
        return render(request, 'To_do_app/register.html')

    def post(self, request):
        #now we need to go back to the template register otherwise we won't be able to create th user in the database
        data = request.POST,
        stuff_for_frontend = {

              'data' : data,
              'has_error':False,

        }

        #now check if the passwords are provided
        password = request.POST.get('password')
        if len(password)<6:
            messages.add_message(request,messages.ERROR, 'Password should be atleast 6 characters long')
            stuff_for_frontend['has_error'] = True

        #now we need to validate the email address entered by the user so inorder to do that we need to install validate-email module from pip repository
        #type pip3 install validate-email in your terminal
        email = request.POST.get('email')
        #now check if the email address is valid or not
        if not validate_email(email):
            messages.add_message(request,messages.ERROR, 'Email not valid!')
            stuff_for_frontend['has_error'] = True

        #check if the email is taken
        #to find out if the user exsists or not in our database if yes then return user name taken use .exists() function to do the job
        if User.objects.filter(email=email).exists():
            messages.add_message(request,messages.ERROR, 'Email is taken')
            stuff_for_frontend['has_error'] = True
        #now check if there is any error in the user input
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            messages.add_message(request,messages.ERROR, 'Username is taken')
            stuff_for_frontend['has_error'] = True

        print(data)
        if stuff_for_frontend['has_error']:
            return render(request, 'To_do_app/register.html', stuff_for_frontend, status=400) #here if we set status to 400 that meands we can prevent the user profile from being created in the database if the error is generated if any of our test condition fails


        #now create the user in the database
        user = User.objects.create_user(username=username, email=email)
        #now set the password for that user and store it in the database
        user.set_password(password)
        #set active user to false so that they don't accidentally get logged in before the email verification process is complete
        user.is_active=False
        #now save the user
        user.save() # now we can say that the user account is successfully created
        #now add a message informing the user that their account has been created successfully
        messages.add_message(request,messages.SUCCESS, 'Account is created successfully')

        #send the verification link to the user's email address
        #step1. construct a url that is unique to the application that we've built so we need the the current domain that our application is running on
        #       and we will set it dynamically we can import this:- from django.contrib.sites.shortcuts import get_current_site
        current_site = get_current_site(request) #get_current_site(request) will give us the current domain of our website dinamically
        #step2. create an email subject
        email_subject= 'Email verification'

        #step3. construct a message
        # so inorder to do that you need to import :- from django.template.loader import render_to_string this library renders a template with a context automatically
        #convert the user.pk into bytes so we need to import:- from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
        #import a module that generated a unique token for our application when we need to verify the user's email address :- from django.contrib.auth.tokens import PasswordResetTokenGenerator it can be used to activate accounts and to reset password
        create_a_context_for_front_end={
            'user':user,
            'domain':current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generated_token.make_token(user),
        }
        message = render_to_string('To_do_app/activate.html',create_a_context_for_front_end)
        #step4. send an email for authentation of the account import :- from django.core.mail import EmailMessage and import settings :- from django.conf import settings
        '''
        email_message = EmailMessage(
           email_subject,            #subject of the email
           message,                  #message that you want to send via email
           settings.EMAIL_HOST_USER, #EMAIL_HOST = 'smtp.gmail.com' that is being imported from the settings.py of the django project
           [email],                  #email adderess entered by the user in the regitration form in the front end of the application of the django project
        )
        '''
        email_message = EmailMessage(
           email_subject,
           message,
           settings.EMAIL_HOST_USER,
           [email],
        )
        email_message.send()
        #now redirect user to the login page
        return redirect('login')

class ActivateAccountView(View):
    def get(self, request,uidb64,token):
        print(f"request = {request}")
        #in here we will check if the token is valid or not
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            print(f"uid = {uid}")
            #do not use User.objects.filter(pk=uid).exists(): instead use User.objects.get(pk=uid) otherwise when you
            #deploy your application on heroku it will throuw an exception
            user = User.objects.get(pk=uid)
            print(f"user = {user}")
        except User.DoesNotExist:
            user = None

        #now check the user before activating them
        if user is not None and generated_token.check_token(user,token):
            print(f"token = {token}")
            #now activate the user in the database for operational ready i.e user now have the permission to use the web Application
            user.is_active = True
            print(f"user active stauts = {user.is_active}")
            user.save()
            messages.add_message(request,messages.INFO,'account activated successfully')
            return redirect('login')
        return render(request,'To_do_app/error.html', status=401)

class LogoutView(View):
    #to handle the get request
    #to handle the get request
    def post(self, request):
        return redirect('login')

class DeveloperView(View):
    #this class will be responsible for showing the developer page
    def get(self, request):
        return render(request, 'To_do_app/dev.html')

'''
create a class named TaskList and inherit the ListView
and this ListView is supposed to return back a template with a query set of data

bydefault class ListView looks for the template named yourAppName_list.html
so we need to change that and configure the class to use our custome template here in my case it is index.html

so the class TaskList has inherited all the functionality of a ListView parent class
ListView parent class will search the template named task_list.html in the directory
To_do(project_name)/To_do_app(app_name)/templates/To_do_app(folder name)/task_list.html
note you should create the file in this directory only otherwise the django project will crash

LoginRequiredMixin will ristrict the list of task to appear only before those users who are logged in
and not before those who are not
if the user is already logged in then by default django will try to go to this url
accounts/login/?next=/
but we want our cutome url here so we have to go to settings.py in our django project
to override the LoginRequiredMixin so that we can use our custom url
'''
class TaskList(LoginRequiredMixin, ListView):
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
    so we need to restrict the users from seeing eah others data because we are pulling all the data from the
    database regardless of the person logged in so we need to change that
    we are trying to ensure that the user can only get the data that they owns

    **kwargs means we are passing in the inital value
    '''
    def get_context_data(self, **kwargs):
        '''now set the context value pass in extra context that needs to be rendered on the page'''
        context = super().get_context_data(**kwargs) #this will be set to the original value and making sure that we are inheriting from the original item
        #now we can start setting up the values here we are modifying context_object_name data
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        return context

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
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'To_do_app/task.html'

'''
createView has more complex logic because we are actually sending a post request to create an item
by default the CreateView is gonna look for task_form.html
'''
class TaskCreate(LoginRequiredMixin, CreateView):
     model = Task

     '''
     by default the CreateView uses model form to work with
     it's basically a class represntation of a Form based on a model so it's gonna take the Task Model from models.py of our application in the
     django project and create all the fields by default

     here we wanna list out all of the fields in our from so
     fields = '__all__' will list out all of the items in the field
     '''
     fields = ['title','discription','complete']

     '''
     so I also wann make sure that we can redirect the user successfully to a different page so we also need to add this to our
     createView

     so in here we need to set the attribute of sucess_url
     if everything goes correctly then go ahead and redirect user to 'task'
     when we create an item just send that user back to the list
     '''
     success_url = reverse_lazy('tasks')

     '''
     override a method called form valid in this class based view
     '''
     def form_valid(self, form):
         '''
         this for_valid will get triggered by default during the post request we need to change that so that
         users can only modify their data and not other's data
         '''
         form.instance.user = self.request.user
         print(str(form.instance.user))
         return super(TaskCreate, self).form_valid(form)

'''
this UpdateView is supposed to take in an item and its supposed to prefill an form
and once we submit it is supposed to modify the data in the database
bydefault this UpdateView will look for the template named model_name_form.html here in my case it will look for
task_form.html
'''
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task

    '''
    by default the CreateView uses model form to work with
    it's basically a class represntation of a Form based on a model so it's gonna take the Task Model from models.py of our application in the
    django project and create all the fields by default

    here we wanna list out all of the fields in our from so
    fields = '__all__' will list out all of the items in the field
    '''
    fields = ['title','discription','complete']

    '''
    so I also wann make sure that we can redirect the user successfully to a different page so we also need to add this to our
    createView

    so in here we need to set the attribute of sucess_url
    if everything goes correctly then go ahead and redirect user to 'task'
    when we create an item just send that user back to the list
    '''
    success_url = reverse_lazy('tasks')

'''
the DeleteView is supposed to be like a confirmation page
it does two things it renders out the confirmation page that says Are you sure that you want to delete this item?
and then when we send a post request it's gonna delete that item

by default the DeleteView is gonna look for a template with the name of model_name_confirm_delete.html
here in my case it will be task_confirm_delete.html
'''
class Delete(LoginRequiredMixin, DeleteView):
    model = Task
    '''
    by default context_object_name will be object
    but here i am going to set that to my custome object name using context_object_name = 'task'
    '''
    context_object_name = 'task'
    '''once we delete an item we want to redirect our user to the home page that contains the list of tasks'''
    success_url = reverse_lazy('tasks')
