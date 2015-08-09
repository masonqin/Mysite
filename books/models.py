from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField()

class DouBanBook(models.Model):
    topNum = models.CharField(max_length=100)
    picLink = models.URLField()
    itemLink = models.URLField()
    titleMain = models.CharField(max_length=100)
    titleSec = models.CharField(max_length=100,blank=True)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    pubdate = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    score = models.CharField(max_length=100)
    evaluation = models.CharField(max_length=100)



