from django.shortcuts import render
from django.http import JsonResponse
from django.views import View #import generic view class
#from .models import Order


# Create your views here.
class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request,  'main/index.html')

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main/about.html')


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