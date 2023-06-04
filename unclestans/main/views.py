from django.shortcuts import render
from django.http import JsonResponse
from django.views import View #import generic view class
from .models import MenuItem, OrderModel
from django.views.generic import TemplateView
import csv



from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
import csv

from .models import MenuItem

# Create your views here.
class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main/index.html')

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main/about.html')

def load_menu(file_path):
    with open(file_path, 'r') as csv_file:
        csv_data = csv.DictReader(csv_file)

        for row in csv_data:
            name = row['name']
            description = row['description']
            price = row['price']
            category = row['category']

            menu_item = MenuItem(name=name, description=description, price=price)
            menu_item.save()
            menu_item.category.set([category])  # Assign the category using set()

class MenuView(TemplateView):
    template_name = 'main/menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not MenuItem.objects.exists():
            # Load the menu data if no menu items exist in the database
            menu_file = "data/menu.csv"
            load_menu(menu_file)

        # Retrieve the menu items from the database
        menu_items = MenuItem.objects.all()
        context['menu_items'] = menu_items

        return context

class Order(View):
    def get(self, request, *args, **kwargs):
        packs = MenuItem.objects.filter(category__name__contains='packs')
        platterfor5 = MenuItem.objects.filter(category__name__contains='platter for 5')
        platterfor10 = MenuItem.objects.filter(category__name__contains='platter for 10')
        extras = MenuItem.objects.filter(category__name__contains='extras')

        # Pass the menu items to the template context
        context = {
            'packs': packs,
            'platterfor5': platterfor5,
            'platterfor10': platterfor10,
            'extras': extras
        }

        # Render the template with the provided context
        return render(request, 'main/order.html', context)
    
    def post(self, request, *args, **kwargs):
        order_items = {
            'items': []   #empty list to store order items
        }
        #create list of selected items
        items = request.POST.getlist('items[]')
        #iterate through the list of itemsnd grab data needed using pk
        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name' : menu_item.name,
                'description': menu_item.description,
                'price': menu_item.price
            }
            order_items['items'].append(item_data)
            price = 0
            item_ids = []

            for item in order_items['items']:
                price += item['price']
                item.ids.append(item['id'])
            customer_name = input("Name:")
            order = OrderModel.objects.create(price=price, customer_name=customer_name)
            order.items.add(*item_ids)




'''def create_order(request):
    if request.method == 'POST':
        # Retrieve the data from the request
        customer_name = request.POST.get('customer_name')
        items = request.POST.get('items')
        quantity = request.POST.get('quantity')

        # Create a new order object
        order = Order(customer_name=customer_name, items=items, quantity=quantity)
        order.save()

        # Return a JSON response indicating success
        return JsonResponse({'status': 'success'})
    else:
        # Return an error response for invalid request method
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
'''