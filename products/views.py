from django.shortcuts import render

def homepage(request):
    
    context = {
        'welcome': 'Welcome to our products homepage'
    }
    
    return render(request, 'products/homepage.html', context)