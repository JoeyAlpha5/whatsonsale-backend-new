from django.db import models
from datetime import datetime
category_choices = [("Clothing","Clothing"), ("Food & Home Care", "Food & Home Care"), ("Electronics", "Electronics"),("Restuarants","Restuarants"),("Banks","Banks"),("Entertainment", "Entertainment")]
product_choices = [("---", "---"),("Denim","Denim"), ("Food", "Food"), ("Jackets", "Jackets"), ("Sneakers", "Sneakers"),("Bags","Bags"),("T-shirt","T-shirt"),("Shoes","Shoes"),("Electronics","Electronics")]
# Create your models here.
class userAccount(models.Model):
    user_id = models.CharField(max_length=250)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    profile_image = models.CharField(max_length=100)
    accept_shared_baskets = models.BooleanField(default=True)
    mobile_number = models.BigIntegerField(default=0,blank=True)
    date = models.DateTimeField(default=datetime.now)
    # welcome_message = models.BooleanField(default=False)
    objects = models.Manager()

class brand(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    category = models.CharField(max_length=50, choices=category_choices, default="")
    logo = models.CharField(max_length=100)
    website = models.URLField(max_length=250,blank=True)
    objects = models.Manager()

class post(models.Model):
    title = models.CharField(max_length=50) 
    post_cover = models.URLField(max_length=250,blank=True)
    video = models.BooleanField(blank=False,default=False)
    description = models.CharField(max_length=150)
    brand = models.ForeignKey(brand, on_delete=models.CASCADE, default="")
    date = models.DateTimeField(auto_now_add=True )
    active = models.BooleanField(default=True)
    objects = models.Manager()

class postCatalogue(models.Model):
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    image = models.URLField(max_length=250,blank=True)
    objects = models.Manager()

class postProduct(models.Model):
    name = models.CharField(max_length=150)
    previous_price = models.FloatField()
    ##sale price
    price = models.FloatField()
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    product_type = models.CharField(choices=product_choices, max_length=50, default="")
    image = models.URLField(max_length=250,blank=True)
    objects = models.Manager()

class postLike(models.Model):
    user = models.ForeignKey(userAccount, on_delete=models.CASCADE)
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
    objects = models.Manager()

class postView(models.Model):
    user = models.ForeignKey(userAccount, on_delete=models.CASCADE)
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
    objects = models.Manager()

class userFollowing(models.Model):
    user = models.ForeignKey(userAccount, on_delete=models.CASCADE)
    brand = models.ForeignKey(brand, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
    objects = models.Manager()

class news(models.Model):
    news_headline = models.CharField(max_length=150)
    news_description = models.TextField()
    news_video = models.CharField(max_length=150)
    news_image = models.DateTimeField(default=datetime.now)
    news_date = models.DateTimeField(auto_now_add=True )
    objects = models.Manager()

class basket(models.Model):
    user = models.ForeignKey(userAccount, on_delete=models.CASCADE)
    product = models.ForeignKey(postProduct, on_delete=models.CASCADE)
    objects = models.Manager()


class basketShare(models.Model):
    basket_owner = models.ForeignKey(userAccount,on_delete=models.CASCADE)
    basket_friend = models.CharField(max_length=150)
    viewed_by_friend = models.BooleanField()
    objects = models.Manager()