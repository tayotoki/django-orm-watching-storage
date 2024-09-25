from django.db.models import F
from django.shortcuts import render

from datacenter.models import Visit


def storage_information_view(request):
    non_closed_visits = (
        Visit.objects
        .still_not_leaved()
        .annotate_inside_duration()
        .annotate_visit_is_strange()
        .annotate(
            who_entered=F("passcard__owner_name")
        )
        .select_related("passcard")
    )

    context = {
        "non_closed_visits": non_closed_visits,
    }
    return render(request, "storage_information.html", context)
