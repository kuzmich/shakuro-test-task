import json

from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Publisher, Shop, Book, BookInShop


def shop_list(request, pid):
    get_object_or_404(Publisher, pk=pid)

    qs = Shop.objects.filter(bookinshop__book__publisher__pk=pid) \
                     .annotate(sold_counter=Sum('bookinshop__sold_counter')) \
                     .order_by('-sold_counter')

    shops = [{'id': shop.id,
              'name': shop.name,
              'books_sold_count': shop.sold_counter}
             for shop in qs]

    for shop in shops:
        qs = BookInShop.objects.filter(shop_id=shop['id'], book__publisher_id=pid).select_related('book')
        shop['books_in_stock'] = [{'id': bookinshop.book.id,
                                   'title': bookinshop.book.name,
                                   'copies_in_stock': bookinshop.in_stock_counter}
                                  for bookinshop in qs]

    return JsonResponse({'shops': shops})


def mark_as_sold(request, shop_id, book_id):
    bs = get_object_or_404(BookInShop, shop_id=shop_id, book_id=book_id)
    payload = json.loads(request.body)

    if bs.in_stock_counter < payload['sold']:
        return JsonResponse({'message': 'Not enough books in stock'}, status=400)

    bs.sold_counter += payload['sold']
    bs.in_stock_counter -= payload['sold']
    bs.save()

    return JsonResponse({})
