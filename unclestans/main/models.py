from django.db import models

# Create your models here.
from django.db import models

class OrderModel(models.Model):
    items = models.ManyToManyField('MenuItem', related_name='order', blank=True)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    streer = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=15, blank=True)
    zipcode = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} - {self.created_at.strftime('%b %d %I %M %p')}"

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    category = models.ManyToManyField('Category', related_name='item')

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Cart(models.Model):
    items = models.ManyToManyField(MenuItem)

    def calculate_total(self):
        return sum(item.price for item in self.items.all())
    
# models.py

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"CartItem {self.pk} - Menu Item: {self.menu_item.name}, Quantity: {self.quantity}"
