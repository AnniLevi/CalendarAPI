from django.core.management.base import BaseCommand
from event_reminder.models import Country, Holiday
from django.db.models import Q
from ics import Calendar
import requests
import arrow


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-c', '--country_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        if options['country_ids']:
            countries = Country.objects.filter(Q(pk__in=options['country_ids']))
        else:
            countries = Country.objects.all()
        success_countries = []
        error_countries = []
        for country in countries:
            try:
                url = "https://www.officeholidays.com/ics-clean/" + country.name
                holidays = list(Calendar(requests.get(url).text).events)
                holidays.sort(key=lambda x: x.begin)
            except Exception:
                error_countries.append(country.name)
                continue

            for holiday in holidays:
                Holiday.objects.create(
                    country_id=country.id,
                    name=holiday.name,
                    date_start=arrow.get(holiday.begin).format('YYYY-MM-DD'),
                    date_end=arrow.get(holiday.end).format('YYYY-MM-DD')
                )
            success_countries.append(country.name)

        if success_countries:
            self.stdout.write(self.style.SUCCESS(f'Successfully recorded holidays for the countries: {success_countries}'))
        if error_countries:
            self.stdout.write(self.style.ERROR(f'Failed parse for the countries: {error_countries}'))


# python manage.py get_holidays -c 3 4 5      - для конкретных стран
# python manage.py get_holidays               - для всех стран
