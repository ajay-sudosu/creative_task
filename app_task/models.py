from django.db import models
from authentication.models import User
from multiselectfield import MultiSelectField


# Create your models here.

class ItemOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # item_order = MultiSelectField(null=True, blank=True, max_choices=100, max_length=100)
    item_order = models.CharField(null=True, blank=True, max_length=100)


class Items(models.Model):
    name = models.CharField(max_length=100)
    # user = models.ForeignKey(User, on_delete=models.SET, null=True, blank=True)
    # item = models.ForeignKey(ItemOrder, on_delete=models.SET, null=True, blank=True)
