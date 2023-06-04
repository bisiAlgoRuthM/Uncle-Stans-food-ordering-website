import os
import django

from django.conf import settings
from main.models import MenuItem

import csv
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Import CSV data into the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        with open(file_path, 'r') as csv_file:
            csv_data = csv.DictReader(csv_file)
            for row in csv_data:
                name = row['name']
                description = row['description']
                price = row['price']
                # Create a new MenuItem instance and save it to the database
                MenuItem.objects.create(name=name, description=description, price=price)
                

