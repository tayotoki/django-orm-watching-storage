from django.db.models import QuerySet, Func, F, Value, CharField, Case, When, Q, DurationField
from django.utils.timezone import localtime

from .constants import DURATION_TO_BE_STRANGE


class PasscardQueryset(QuerySet):
    def active(self):
        """Активные карты доступа"""

        return self.filter(is_active=True)


class VisitQueryset(QuerySet):
    def still_not_leaved(self):
        """Визиты без времени выхода"""

        return self.filter(leaved_at__isnull=True)

    def annotate_inside_duration(self):
        """Время нахождения внутри хранилища"""

        return self.annotate(
            inside_duration=Func(
                localtime() - F("entered_at"),
                Value("HH:MM:SS"),
                function="to_char",
                output_field=CharField()
            )
        )

    def annotate_visit_is_strange(self):
        """Был ли визит подозрительным"""

        return self.annotate(
            full_duration=F("leaved_at") - F("entered_at"),
            inside_duration=localtime() - F("entered_at"),
            is_strange=Case(
                When(
                    Q(
                        full_duration__gt=DURATION_TO_BE_STRANGE,
                        leaved_at__isnull=False
                    )
                    | Q(
                        inside_duration__gt=DURATION_TO_BE_STRANGE,
                    ),
                    then=True
                ),
                default=False,
                output_field=DurationField(),
            )
        )
