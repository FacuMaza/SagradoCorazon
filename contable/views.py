from django.shortcuts import render

# Create your views here.
def contable(request):
    return render(request, "indexcontable.html")