from django.shortcuts import render

from datacenter.models import Passcard


def active_passcards_view(request):
    active_passcards = Passcard.objects.active()
    context = {
        "active_passcards": active_passcards,
    }
    return render(request, "active_passcards.html", context)
