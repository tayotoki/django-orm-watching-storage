from django.shortcuts import render

from datacenter.models import Passcard


def active_passcards_view(request):
    # Программируем здесь

    all_passcards = Passcard.objects.is_active()
    context = {
        'active_passcards': all_passcards,  # люди с активными пропусками
    }
    return render(request, 'active_passcards.html', context)
