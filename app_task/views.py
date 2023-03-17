from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .models import Items, ItemOrder, User
from django.db.models import Case, When
from django.http import HttpResponse
from django.contrib import messages
from django.views import View
import json


def change_strind_to_int(i):
    """

    :param i: Element of the iterable which is a string.
    :return: Integer element.
    """
    return int(i)


def show_items(request):
    """
    :param request: Request object.
    :return: List of items according to the order saved by user.
    """
    if request.method == "GET":
        try:
            item_order_id = ItemOrder.objects.get(user=request.user.id)
            order_list = list(map(change_strind_to_int, json.loads(item_order_id.item_order)))
            ordering = Case(*[When(id=id_val, then=index) for index, id_val in enumerate(order_list)])
            items = Items.objects.filter(id__in=order_list).order_by(ordering)
        except Exception as e:
            items = Items.objects.all()
        context = {'items': items}
        return render(request, 'home.html', context)


def update_order(request):
    """
    :param request: Request object.
    :return: Function to save order of items a user is choosing.
    """
    try:
        if request.method == 'POST':
            queryset = dict(request.POST)
            order = queryset.get("order[]")
            user_id = request.user.id
            try:
                ItemOrder.objects.get(user=user_id)
                item_order_obj = ItemOrder.objects.filter(user=request.user).update(item_order=json.dumps(order))
            except Exception as e:
                item_order_obj = ItemOrder.objects.create(user=request.user, item_order=json.dumps(order))
            return HttpResponse('Success.')
        else:
            return HttpResponse('Invalid request.')
    except Exception as error:
        print(error)


class AddItem(View):
    """
    Class that handles add-item from a user or fetch items of a particular user.
    """
    def get(self, request):
        return render(request, "add-item.html")

    def post(self, request):
        itemname = request.POST.get("itemname")
        if not request.POST.get("itemname"):
            messages.error(request, 'Please fill the item name')
            return render(request, "add-item.html")
        items = Items.objects.create(name=itemname)
        item_id = items.id
        try:
            item_order_obj = ItemOrder.objects.get(user=request.user)
            item_order_list = json.loads(item_order_obj.item_order)
            item_order_list.insert(0, item_id)
            ItemOrder.objects.filter(user=request.user).update(item_order=json.dumps(item_order_list))
        except Exception as error:
            item_order_list = [i.id for i in Items.objects.all()] + [item_id]
            ItemOrder.objects.create(user=request.user, item_order=json.dumps(item_order_list))
        return redirect('home')

