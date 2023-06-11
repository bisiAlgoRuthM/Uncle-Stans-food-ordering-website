from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MenuForm
from main.models import MenuItem

def upload_view(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu_item_detail', item_id=id, success=True)
    else:
        form = MenuForm()

    return render(request, 'resturant/upload_menu.html', {'form': form})

def update_view(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('menu_item_detail', item_id=item.id, success=True)
    else:
        form = MenuForm(instance=item)

    return render(request, 'resturant/update_menu.html', {'form': form})

def menu_item_detail(request, item_id, success):
    item = get_object_or_404(MenuItem, id=item_id)
    success = request.GET.get('success', False)
    return render(request, 'menu_item_detail.html', {'item': item, 'success': success})