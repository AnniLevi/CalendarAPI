from django.core.management.base import BaseCommand, CommandError

import requests
from bs4 import BeautifulSoup
from event_reminder.models import Country


class Command(BaseCommand):
    def handle(self, *args, **options):
        url = 'https://www.officeholidays.com/countries/index.php'
        response = requests.get(url)
        if response.status_code != 200:
            raise CommandError(f'Unable to get data, status {response.status_code}')
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find_all('div', class_='four omega columns')
        countries = []
        for item in data:
            country = item.text.strip('\n\n\n\xa0\xa0').split('\n\n\n\xa0\xa0')
            countries.extend(country)

        Country.objects.bulk_create([Country(name=name) for name in countries])
        self.stdout.write(self.style.SUCCESS('Countries are successfully recorded in the database'))


# python manage.py get_countries
