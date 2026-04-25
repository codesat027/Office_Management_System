from django.shortcuts import render
from .models import Notice


def notice_list(request):
    notices = Notice.objects.order_by('-created_at')[:5]
    return render(request, 'notices/list.html', {'notices': notices})