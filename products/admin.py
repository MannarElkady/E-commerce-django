from django.contrib import admin
from .models import Item, Category,Comment,Cart

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Cart)
