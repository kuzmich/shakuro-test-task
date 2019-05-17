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
    resp = client.get('/api/publishers/{}/shops'.format(addison_wesley.id))
    print(resp.json())
    assert resp.status_code == 200

    # Then the endpoint returns list of shops selling at least one book of that publisher,
    # ordered by the number of books sold, and for each shop it should include
    # the list of Publisher’s books that are currently in stock.
    shops = resp.json()['shops']

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

