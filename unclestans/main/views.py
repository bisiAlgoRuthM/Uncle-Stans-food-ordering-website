from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View #import generic view class
from .models import MenuItem, OrderModel, Category
from django.views.generic import TemplateView
import csv
from decimal import Decimal
from django.views.decorators.http import require_POST
from .models import MenuItem, OrderModel

# Create your views here.
class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main/index.html')

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main/about.html')
class Entree(View):
    def get(self, request, *args, **kwargs):
        
        pack = MenuItem.objects.filter(category__name__contains='pack')
        platter = MenuItem.objects.filter(category__name__contains='platter')
        drink = MenuItem.objects.filter(category__name__contains='drink')
        extra = MenuItem.objects.filter(category__name__contains='extra')

        # Pass the menu items to the template context
        context = {
            'pack': pack,
            'platter': platter,
            'extra': extra,
            'drink': drink
        }

        # Render the template with the provided context
        return render(request, 'main/entree.html', context)

'''class Test(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main/test.html')'''
    
def load_menu(file_path):
    with open(file_path, 'r') as csv_file:
        csv_data = csv.DictReader(csv_file)

        for row in csv_data:
            name = row['name']
            description = row['description']
            price = row['price']


            menu_item = MenuItem(name=name, description=description, price=price)
            menu_item.save()

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
        menu_items_data = []
        for item in menu_items:
            menu_item_data = {
                'name': item.name,
                'description': item.description,
                'image_url': item.image.url if item.image else '',
                'price': item.price
            }
            menu_items_data.append(menu_item_data)

        context['menu_items'] = menu_items_data

        return context
    
from django.shortcuts import get_object_or_404, redirect
from .models import MenuItem

def update_quantity(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = request.POST.get('quantity')

        # Retrieve the MenuItem object
        menu_item = get_object_or_404(MenuItem, id=item_id)

        # Update the quantity
        menu_item.quantity = quantity
        menu_item.save()

        # Redirect to the cart page
        return redirect('cart')




class Order(View):
    def get(self, request, *args, **kwargs):
        pack = MenuItem.objects.filter(category__name__contains='pack')
        platter = MenuItem.objects.filter(category__name__contains='platter')
        drink = MenuItem.objects.filter(category__name__contains='drink')
        extra = MenuItem.objects.filter(category__name__contains='extras')

        # Pass the menu items to the template context
        context = {
            'pack': pack,
            'platter': platter,
            'extra': extra,
            'drink': drink
        }

        # Render the template with the provided context
        return render(request, 'main/order.html', context)
    
    def post(self, request, *args, **kwargs):
        order_items = []
        #create list of selected items
        items = request.POST.getlist('items[]')
        quantity = request.POST.getlist('quantity[]')

        #iterate through the list of item, grab data needed using pk
        for item, quantity in zip(items, quantity):
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name' : menu_item.name,
                'description': menu_item.description,
                'price': menu_item.price,
                'quantity': int(quantity)
            }
            order_items.append(item_data)
            total_price = sum(item['price'] * item['quantity'] for item in order_items)
            item_ids = [item['id'] for item in order_items]

            order = OrderModel.objects.create(price=total_price)
            order.items.add(*item_ids)

            cart = request.session.get('cart', [])
            cart.extend(item_ids)
            request.session['cart'] = cart


            context = {
                'items': order_items,
                'price':total_price
            }

            return redirect('cart')

@require_POST
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', [])

    if item_id in cart:
        cart.remove(item_id)
        request.session['cart'] = cart

    return redirect('cart')


def cart_view(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        remove_from_cart(request, item_id)

    cart = request.session.get('cart', [])
    total = Decimal(0)

    # Retrieve items in the cart
    order_items = MenuItem.objects.filter(pk__in=cart)

    # Calculate the total price
    for item in order_items:
        item.quantity = cart.count(item.pk)
        total += item.price * item.quantity

    context = {
        'menu_items': order_items,
        'price': total,
        'total': total
    }

    return render(request, 'main/cart.html', context)


class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))

        try:
            item = MenuItem.objects.get(pk=item_id)
        except MenuItem.DoesNotExist:
            return redirect('order')  # Redirect to the order page if the item does not exist

        cart = request.session.get('cart', {})
        if item_id in cart:
            cart[item_id] += quantity
        else:
            cart[item_id] = quantity

        request.session['cart'] = cart

        # Retrieve the menu items for the order page
        pack = MenuItem.objects.filter(category__name__contains='pack')
        platter = MenuItem.objects.filter(category__name__contains='platter')
        drink = MenuItem.objects.filter(category__name__contains='drink')
        extra = MenuItem.objects.filter(category__name__contains='extras')

        context = {
            'pack': pack,
            'platter': platter,
            'extra': extra,
            'drink': drink
        }

        return render(request, 'main/order.html', context)


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
'''            category_name = row['category']

            category, _ = Category.objects.get_or_create(name=category_name)'''


from django.views.generic import TemplateView
from main.models import MenuItem, Category

'''class MenuView(TemplateView):
    template_name = 'main/menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs )

        if not MenuItem.objects.exists():
            # Load the menu data if no menu items exist in the database
            menu_file = "data/menu.csv"
            load_menu(menu_file)

        # Retrieve the menu items from the database grouped by category
        categories = Category.objects.all()
        menu_items_data = {}

        for category in categories:
            menu_items = MenuItem.objects.filter(category=category)
            menu_items_data[category.name] = menu_items

        context['menu_items_data'] = menu_items_data

        return context'''
