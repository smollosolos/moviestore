from django.shortcuts import render
from cart.models import Item
from movies.models import Review
from collections import defaultdict
from django.contrib.admin.views.decorators import staff_member_required

def index(request):
    template_data = {}
    template_data['title'] = 'Movies Store'
    return render(request, 'home/index.html', {
        'template_data': template_data})
def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'home/about.html', {'template_data' : template_data})

@staff_member_required
def engagement(request):
    template_data = {}
    template_data['title'] = 'View Engagement'

    reviews = Review.objects.all()
    dictr = defaultdict(list)
    movie1 = None
    maxlen = -1

    for r in reviews:
        dictr[r.movie].append(r)
        if len(dictr[r.movie]) > maxlen:
            maxlen = len(dictr[r.movie])
            movie1 = r.movie

    items = Item.objects.all()
    dictb = defaultdict(int)
    dicti = defaultdict(list)
    movie2 = None
    maxlen = -1

    for i in items:
        dictb[i.movie] += i.quantity
        if dictb[i.movie] > maxlen:
            maxlen = dictb[i.movie]
            movie2 = i.movie
        dicti[i.movie].append(i)

    template_data['movie1'] = movie1
    template_data['reviews'] = dictr[movie1] if movie1 else []
    template_data['movie2'] = movie2
    template_data['items'] = dicti[movie2] if movie2 else []
    
    return render(request, "home/engagement.html", {'template_data' : template_data})
