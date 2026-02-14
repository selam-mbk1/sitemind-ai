# rag/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def rag_home(request):
    return render(request, 'rag/rag_home.html')
