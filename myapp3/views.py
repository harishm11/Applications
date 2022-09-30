from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
import tabula, os
import pandas as pd

def home(request):
    return render(request, 'base.html')