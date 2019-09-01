from django.shortcuts import render
from bhavdata import BhavData
# Create your views here.

DATA = BhavData()
DATA.parse()
DATA = DATA.content


def index(request):
    return render(request, "base.html", {"data": DATA})
