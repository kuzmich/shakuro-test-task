from django.urls import reverse
from model_mommy import mommy
import pytest


@pytest.mark.django_db
def test_list_of_shops(client):
    # Given there're a few shops that selling some books
    addison_wesley = mommy.make('Publisher', name='Addison–Wesley')
    microsoft_press = mommy.make('Publisher', name='Microsoft Press')
    mit_press = mommy.make('Publisher', name='The MIT Press')

    tdd = mommy.make('Book', name='Test-driven development by example', publisher=addison_wesley)
    man_month = mommy.make('Book', name='The Mythical Man-Month', publisher=addison_wesley)
    sicp = mommy.make('Book',
                      name='Structure and Interpretation of Computer Programs',
                      publisher=mit_press)
    code_complete = mommy.make('Book', name='Code Complete', publisher=microsoft_press)

    amazon = mommy.make('Shop', name='Amazon')
    hive = mommy.make('Shop', name='Hive')
    wordery = mommy.make('Shop', name='Wordery')

    amazon.books.add(tdd, through_defaults={'sold_counter': 100, 'in_stock_counter': 200})
    amazon.books.add(man_month, through_defaults={'sold_counter': 500, 'in_stock_counter': 2000})
    amazon.books.add(code_complete, through_defaults={'sold_counter': 200, 'in_stock_counter': 500})
    hive.books.add(sicp, through_defaults={'sold_counter': 30, 'in_stock_counter': 70})
    wordery.books.add(code_complete, through_defaults={'sold_counter': 50, 'in_stock_counter': 50})
    wordery.books.add(man_month, through_defaults={'sold_counter': 90, 'in_stock_counter': 30})

    # When someone asks for a list of shops that sell publisher's book
    resp = client.get(reverse('api:shop_list', kwargs={'pid': addison_wesley.id}))
    print(resp.json())
    assert resp.status_code == 200

    # Then the endpoint returns list of shops selling at least one book of that publisher,
    # ordered by the number of books sold, and for each shop it should include
    # the list of Publisher’s books that are currently in stock.
    shops = resp.json()['shops']
    assert len(shops) == 2

    assert (
        {'id': amazon.id,
         'name': amazon.name,
         'books_sold_count': 600,
         'books_in_stock': [
             {'id': tdd.id,
              'title': tdd.name,
              'copies_in_stock': 200},
             {'id': man_month.id,
              'title': man_month.name,
              'copies_in_stock': 2000}
         ]} == shops[0]
    )

    assert (
            {'id': wordery.id,
             'name': wordery.name,
             'books_sold_count': 90,
             'books_in_stock': [
                 {'id': man_month.id,
                  'title': man_month.name,
                  'copies_in_stock': 30}
             ]} == shops[1]
    )


@pytest.mark.django_db
def test_mark_book_as_sold(client):
    from api.models import BookInShop

    # Given a shop sells some books
    book = mommy.make('Book')
    shop = mommy.make('Shop')
    shop.books.add(book, through_defaults={'sold_counter': 30, 'in_stock_counter': 40})

    # When someone requests to mark some copies of the book as sold
    resp = client.patch(
        reverse('api:mark_as_sold', kwargs={'shop_id': shop.id, 'book_id': book.id}),
        {'sold': 10},
        content_type='application/json'
    )
    assert resp.status_code == 200

    # Then this info is stored in the db
    bs = BookInShop.objects.get(shop_id=shop.id, book_id=book.id)
    assert bs.sold_counter == 40
    assert bs.in_stock_counter == 30


@pytest.mark.django_db
def test_mark_book_as_sold__too_many(client):
    from api.models import BookInShop

    # Given a shop sells some books
    book = mommy.make('Book')
    shop = mommy.make('Shop')
    shop.books.add(book, through_defaults={'sold_counter': 30, 'in_stock_counter': 40})

    # When someone requests to mark too many copies of the book as sold
    resp = client.patch(
        reverse('api:mark_as_sold', kwargs={'shop_id': shop.id, 'book_id': book.id}),
        {'sold': 100},
        content_type='application/json'
    )

    # Then API answers with 400 Bad Request
    assert resp.status_code == 400

    # and the info in the db is not changed
    bs = BookInShop.objects.get(shop_id=shop.id, book_id=book.id)
    assert bs.sold_counter == 30
    assert bs.in_stock_counter == 40
