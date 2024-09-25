from django.db.models import QuerySet, Func, F, Value, CharField, Case, When, Q, DurationField
from django.utils.timezone import localtime

from .constants import DURATION_TO_BE_STRANGE


class PasscardQueryset(QuerySet):
    def is_active(self):
        """Активные карты доступа"""

        return self.filter(is_active=True)


class VisitQueryset(QuerySet):
    def not_leaved(self):
        """Визит, не покинувший хранилище"""

        return self.filter(leaved_at__isnull=True)

    def annotate_duration(self):
        """Время нахождения в хранилище"""

        return self.annotate(
            duration=Func(
                localtime() - F("entered_at"),
                Value("HH:MM:SS"),
                function="to_char",
                output_field=CharField()
            )
        )

    def annotate_is_strange(self):
        """Был ли проход подозрительным"""

        return self.annotate(
            duration=F("leaved_at") - F("entered_at"),
            is_strange=Case(
                When(
                    Q(
                        duration__gt=DURATION_TO_BE_STRANGE,
                        leaved_at__isnull=False
                    ),
                    then=True
                ),
                default=False,
                output_field=DurationField(),
            )
        )
