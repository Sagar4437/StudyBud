from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    name = models.CharField(max_length=200) # group name

    def __str__(self) -> str:
        return self.name

# Create your models here.
class Room(models.Model):
    host =  models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL, null=True) # Single topic may have many rooms ==> single to Many RELATIONSHIP
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    participants = models.ManyToManyField(User,related_name='participants',blank=True) # many to many relationship
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-updated','-created']

class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)# one user can do many messages ==> one to many RELATIONSHIP
    room = models.ForeignKey(Room,on_delete=models.CASCADE) #Single room contain many message==> single to Many RELATIONSHIP
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.body[:50]
    
    class Meta:
        ordering = ['-created']