from django.db import models

# Create your models here.
class Login(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100)



class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    image=models.CharField(max_length=300)
    age=models.CharField(max_length=300)
    place=models.CharField(max_length=300)
    pin=models.CharField(max_length=300)
    post=models.CharField(max_length=300)
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)

class Complaint(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.CharField(max_length=100)
    complaint=models.CharField(max_length=300)
    status = models.CharField(max_length=100, default='pending')
    reply = models.CharField(max_length=100, default='pending')


class Feedback(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.CharField(max_length=100)
    feedback=models.CharField(max_length=300)
    rating = models.CharField(max_length=100, default='pending')



class Manufacture(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    image=models.CharField(max_length=300)
    place = models.CharField(max_length=300)
    pin = models.CharField(max_length=300)
    post = models.CharField(max_length=300)
    status = models.CharField(max_length=300)
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)


class Category(models.Model):
    MANUFACTURE=models.ForeignKey(Manufacture,on_delete=models.CASCADE)
    category_name = models.CharField(max_length=100)



class Product(models.Model):
    CATEGORY=models.ForeignKey(Category,on_delete=models.CASCADE)
    MANUFACTURE=models.ForeignKey(Manufacture,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    price=models.CharField(max_length=100)
    description=models.CharField(max_length=300)



