from django.shortcuts import render, get_object_or_404

from datacenter.models import Passcard
from datacenter.models import Visit


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    this_passcard_visits = (
        Visit.objects
        .filter(passcard=passcard)
        .annotate_visit_is_strange()
        .select_related("passcard")
    )

    context = {
        "passcard": passcard,
        "this_passcard_visits": this_passcard_visits
    }
    return render(request, "passcard_info.html", context)
