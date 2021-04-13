from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class User(models.Model):
    Email = models.EmailField(max_length=50)
    Password = models.CharField(max_length=50)
    Role = models.CharField(max_length=50)
    Otp = models.IntegerField(default=123)
    is_created = models.DateTimeField(auto_now_add=True)
    is_updated = models.DateTimeField(auto_now_add=True)
    is_verfied = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

class Customer(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    Firstname = models.CharField(max_length=50)
    Lastname = models.CharField(max_length=50)
    Contact = models.BigIntegerField()
    City = models.CharField(max_length=50)
    State = models.CharField(max_length=50)
    Address = models.CharField(max_length=100)
    Gender = models.CharField(max_length=50)
    pics = models.ImageField(upload_to="img/",default="abc.jpg")
    weblink = models.CharField(max_length=250,default="abc.com")
    sociallink = models.CharField(max_length=250,default="facebook.com")
    zipcode = models.BigIntegerField(default=123)

class Chef(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    Firstname = models.CharField(max_length=50)
    Lastname = models.CharField(max_length=50)
    Contact = models.BigIntegerField()
    City = models.CharField(max_length=50)
    State = models.CharField(max_length=50)
    Address = models.CharField(max_length=100)
    Ability = models.CharField(max_length=200)
    Gender = models.CharField(max_length=50)
    pics = models.ImageField(upload_to="img/",default="abc.jpg")
    weblink = models.CharField(max_length=250,default="abc.com")
    sociallink = models.CharField(max_length=250,default="facebook.com")
    zipcode = models.BigIntegerField(default=123)



class Category(models.Model):
    chef_id = models.ForeignKey(Chef,on_delete=models.CASCADE)
    Productname = models.CharField(max_length=50)
    Description = models.CharField(max_length=50)
    Image = models.ImageField(upload_to="img/")
    Keywords = models.CharField(max_length=50)




class Product(models.Model):
    chef_id = models.ForeignKey(Chef,on_delete=models.CASCADE,default="")
    cat_id = models.ForeignKey(Category,on_delete=models.CASCADE)
    Productname = models.CharField(max_length=50)
    ProductDescription = models.CharField(max_length=5000)
    Price = models.BigIntegerField()
    Expirydate = models.CharField(max_length=50)
    Mfgdate = models.CharField(max_length=50)
    Detail = models.CharField(max_length=5000)
    Image = models.ImageField(upload_to="img/")
    Status = models.CharField(max_length=500)
    Quantity = models.CharField(max_length=50)
    Keywords = models.CharField(max_length=500)
    discount = models.BigIntegerField(default=5)
    Integrates=models.CharField(max_length=5000,default="abc,xyz,uewyvfukerybvfrei")
    is_created = models.DateTimeField(auto_now_add=True)
    is_updated = models.DateTimeField(auto_now_add=True)
    



class Image(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    Title = models.CharField(max_length=50)
    Image = models.ImageField(upload_to="img/")


class Order(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    Ordername = models.CharField(max_length=50)
    Email = models.EmailField(max_length=50)
    Address = models.CharField(max_length=100)
    Contact = models.BigIntegerField()
    Total = models.BigIntegerField()
    Status = models.CharField(max_length=50)
    is_created = models.DateTimeField(auto_now_add=True)
    is_updated = models.DateTimeField(auto_now_add=True)

class Order_product(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    Total = models.BigIntegerField()
    Price = models.BigIntegerField()
    is_created = models.DateTimeField(auto_now_add=True)
    is_updated = models.DateTimeField(auto_now_add=True)

class Faq(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    Question = models.CharField(max_length=200)
    Answer = models.CharField(max_length=200)
    Status = models.CharField(max_length=50)
    is_created = models.DateTimeField(auto_now_add=True)
    is_updated = models.DateTimeField(auto_now_add=True)

class Shopping_cart(models.Model):
    Cust_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
    pro_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    Productname = models.CharField(max_length=200)
    Quantity = models.BigIntegerField()
    Price = models.BigIntegerField()
    Total = models.BigIntegerField()
    is_created = models.DateTimeField(auto_now_add=True)
    is_updated = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    Customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    Rating = models.IntegerField(default=0)
    Description = models.TextField(max_length=500)

class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)

















    




