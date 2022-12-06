
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Person(models.Model):
    profile_pic = models.ImageField(default="Bojack.png", null=True, blank=True)
    user = models.OneToOneField(User,null = True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    



    def __str__(self):
        return self.name

class Channel(models.Model):

    sender = models.OneToOneField(User,null = True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    people = models.ManyToManyField(Person,)
    message_data = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class DirectMessage(models.Model):
    #message sent by this person
    sender = models.ForeignKey(User,null = True, on_delete=models.CASCADE,blank=True)
    #name will can be edited:
    name = models.CharField(max_length=200, null=True,blank=True)
    #many to many but will only have 2 people / who can access this
    both_people = models.ManyToManyField(Person,blank=True)
    #auto display
    message_data = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
   

