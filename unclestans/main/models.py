from django.db import models

# Create your models here.
from django.db import models

class OrderModel(models.Model):
    customer_name = models.CharField(max_length=100)
    items = models.ManyToManyField('MenuItem', related_name='order', blank=True)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name} : {self.created_at.strftime('%b %d %I %M %p')}"

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    category = models.ForeignKey('Category',  on_delete=models.CASCADE, related_name='item', default=1)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
