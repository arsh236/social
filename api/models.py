from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Posts(models.Model):
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=250)
    image=models.ImageField(upload_to="postimages" ,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Commments(models.Model):
    posts=models.ForeignKey(Posts,on_delete=models.CASCADE)
    comment=models.CharField(max_length=120)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.comment