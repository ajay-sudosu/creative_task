from django.urls import path, include
from .views import *

urlpatterns = [
    path('home', show_items, name="home"),
    path('update_order', update_order),
    path('add-item', AddItem.as_view(), name='add-item'),
]
