from django.urls import path
from django.conf.urls import url

'''import TaskList class from views.py into this urls.py file of the application'''
from . views import TaskList, TaskDetail, TaskCreate, TaskUpdate, Delete, CustomLoginView, LogoutView, RegistrationView, ActivateAccountView, DeveloperView

'''we can actually use the views directly
    path('logout/', LogoutView.as_view(next_page = 'login' ), name='logout'), will use the LogoutView directly
    next_page = 'login' means once we press login button in pur front end it should send the user back to the login page
'''
from django.contrib.auth.views import LogoutView

'''
TaskList is a class in our views.py but our urls.py of our app cannot use class in here so we will have to modify
the code for the url from this 'example url =     path('add_todo/',views.add_todo, name="add_todo"),'
to this 'exaple url = path('', TaskList.as_view(), name='tasks'),'

view by default looks for pk value
path('task/<int:pk>/', TaskDetail.as_view(), name='tasks'),
'''
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page = 'login' ), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>', ActivateAccountView.as_view(), name='activate'),
    path('request-reset-email', views.RequestResetEmailView.as_view(), name='request-reset-email'),
    path('set-new-password/<uidb64>/<token>', views.SetNewPasswordView.as_view(), name='set-new-password'),

    path('developer/', DeveloperView.as_view(), name='developer'),

    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('create-task/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', Delete.as_view(), name='task-delete'),

]
