from django.contrib import admin
from .models import Publisher, Book, Shop, BookInShop


admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(Shop)
admin.site.register(BookInShop)
