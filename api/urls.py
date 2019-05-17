from django.urls import path
from .views import shop_list


urlpatterns = [
    path('publishers/<int:pid>/shops', shop_list)
]