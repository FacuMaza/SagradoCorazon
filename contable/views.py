from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.


@login_required
def contable(request):
    return render(request, "indexcontable.html")