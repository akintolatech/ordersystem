from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Estate, Legal

# Create your views here.

def page_not_found(request, exception):
    return render(request, 'authenticator/error.html', status=404)

def index(request):
    estates = Estate.objects.all().order_by("-id")
    estate_count = estates.count()
    print(estate_count)

    context = {
        'estate_count': estate_count,
        'estates': estates,
        'Welcome': 'You are wired!'
    }
    return render(request, "browser/index.html", context)


def detail(request, estate_id):
    estate = get_object_or_404(Estate, pk=estate_id)
    context = {
        'estate': estate
    }
    return render(request, 'browser/pages/detail.html',context)

def detail_app (request, estate_id):
    estate = get_object_or_404(Estate, pk=estate_id)
    context = {
        'estate': estate
    }
    return render(request, 'browser/pages/detail-app.html',context)

def legal (request):
    context = {
        'terms': Legal.objects.all()
    }
    return render(request, 'browser/pages/legal.html', context)