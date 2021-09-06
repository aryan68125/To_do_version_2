from django.urls import path
from django.conf.urls import url

'''import TaskList class from views into this urls.py file of the application'''
from . views import TaskList, TaskDetail

'''
TaskList is a class in our views.py but our urls.py of our app cannot use class in here so we will have to modify
the code for the url from this 'example url =     path('add_todo/',views.add_todo, name="add_todo"),'
to this 'exaple url = path('', TaskList.as_view(), name='tasks'),'

view by default looks for pk value
path('task/<int:pk>/', TaskDetail.as_view(), name='tasks'),
'''
urlpatterns = [
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
]
