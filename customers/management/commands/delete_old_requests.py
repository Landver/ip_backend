from datetime import timedelta, datetime
from django.core.management.base import BaseCommand

from customers.models import EnrolmentRequest


class Command(BaseCommand):
    help = 'Delete old, review-pending enrolment requests'

    def handle(self, *args, **options):
        queryset = EnrolmentRequest.objects.filter(
            created_date__lte=(datetime.now() - timedelta(days=5)),
            review_pending=True
        )

        for obj in queryset:
            obj.delete()

        self.stdout.write(self.style.SUCCESS(f'{len(queryset)} enrolment requests had been deleted'))
