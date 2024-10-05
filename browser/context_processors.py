from .models import Estate, Legal

def product_list(request):
    estates = Estate.objects.all().order_by("-id")
    estate_count = estates.count()

    context = {
        'estate_count': estate_count,
        'estates': estates,
    }
    return context