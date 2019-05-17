from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=255)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=50)
    books = models.ManyToManyField(Book, through='BookInShop')

    def __str__(self):
        return self.name


class BookInShop(models.Model):
    # TODO Unique pair
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    in_stock_counter = models.IntegerField(default=0)
    sold_counter = models.IntegerField(default=0)
