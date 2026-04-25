from django.shortcuts import render
from datetime import date
from .models import BirthdayAnniversary


def birthday_list(request):
    today = date.today()
    active_tab = request.GET.get('tab', 'birthdays')

    birthdays = BirthdayAnniversary.objects.filter(
        event_type='Birthday',
        event_date__month=today.month
    ).order_by('event_date')

    anniversaries = BirthdayAnniversary.objects.filter(
        event_type='Anniversary',
        event_date__month=today.month
    ).order_by('event_date')

    today_event = BirthdayAnniversary.objects.filter(
        event_date__month=today.month,
        event_date__day=today.day
    ).first()

    context = {
        'birthdays': birthdays,
        'anniversaries': anniversaries,
        'today': today,
        'today_event': today_event,
        'active_tab': active_tab,
    }

    return render(request, 'birthday_anniversary/list.html', context)