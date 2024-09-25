from django.db.models import F
from django.shortcuts import render

from datacenter.models import Visit


def storage_information_view(request):
    non_closed_visits = (
        Visit.objects
        .not_leaved()
        .annotate_duration()
        .annotate(
            who_entered=F("passcard__owner_name")
        )
        .select_related("passcard")
    )

    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
