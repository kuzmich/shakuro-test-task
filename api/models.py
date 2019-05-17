from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=50)


class Book(models.Model):
    name = models.CharField(max_length=255)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)


class Shop(models.Model):
    name = models.CharField(max_length=50)
    books = models.ManyToManyField(Book, through='BookInShop')


class BookInShop(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    in_stock_counter = models.IntegerField(default=0)
    sold_counter = models.IntegerField(default=0)
