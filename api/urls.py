from django.urls import path
from .views import shop_list, mark_as_sold


app_name = 'api'
urlpatterns = [
    path('publishers/<int:pid>/shops', shop_list, name='shop_list'),
    path('shops/<int:shop_id>/books/<int:book_id>', mark_as_sold, name='mark_as_sold')
]