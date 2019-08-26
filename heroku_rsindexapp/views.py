from django.shortcuts import render
from bhavdata import BhavData
# Create your views here.

DATA = BhavData()
DATA.download()

def index(request):
    return render(request, "base.html", {"data":DATA.content})
