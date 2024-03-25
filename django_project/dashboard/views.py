from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from item.models import Item

from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    if request.user.is_authenticated:
        items = Item.objects.filter(created_by=request.user)

        return render(request, 'dashboard/index.html', {
            'items': items,
        })


