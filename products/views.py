from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Product

from django.utils import timezone

def homepage(request):
    
    products = Product.objects
    
    context = {
        'products': products
    }
    
    return render(request, 'products/homepage.html', context)

@login_required(login_url="/account/signup")
def create(request):
    if request.method == "POST":
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon'] and request.FILES['image']:
            product = Product()
            product.title = request.POST['title']
            product.body = request.POST['body']
            if request.POST['url'].startswith('https://') or request.POST['url'].startswith('http://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']
            product.icon = request.FILES['icon']
            product.image = request.FILES['image']
            product.pub_date = timezone.datetime.now()
            product.hunter = request.user
            product.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 
                          'products/create.html', 
                          {'error': "You have not filled all the fields"})
    else:
        return render(request, 'products/create.html')
    
def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    context = {
        'product': product
    }
    
    return render(request, 'products/detail.html', context)

@login_required
def upvote(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=product_id)
        product.votes_total += 1
        product.save()
        return redirect('/products/' + str(product.id))