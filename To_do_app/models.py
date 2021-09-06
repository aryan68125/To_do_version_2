from django.db import models

'''
our user by default we want the task to be owned by a specific user
so inorder to do that import the built in django user model
default django user authentication model provided by django
'''
from django.contrib.auth.models import User
# Create your models here.
class Task(models.Model):
    '''
    so in order to achieve 'the task to be owned by a specific user'
    we need to create a one to many relationship
    we can have one user and that user can have many items we will use Foreignkey Model to achieve that

    on_delete will handle the situation if the user deletes his or her account Or the admin deletes the user
    in this situation delete all the tasks associated with the user model.CASCADE does exactly that

    null=True, blank=True adding them is a good practice so that you can save time other wise you will have to deal with unecessary
    headache of dealing with the database related errors
    '''
    user = models.ForeignKey(User, on_delete =models.CASCADE, null=True, blank=True )
    title = models.CharField(max_length=2000)
    discription = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''set the default value to title'''
        return self.title

    class Meta:
        '''
        here we are ordering our model
        whenever we are querying multiple items from the database it will order itself via task completion status
        '''
        ordering = ['complete']
