from django.contrib import admin

# Register your models here
from django.contrib import admin
from books.models import Publisher,Author,Book,DouBanBook

admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(DouBanBook)