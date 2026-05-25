import csv
from datetime import datetime 
from django.core.management.base import BaseCommand
from dispatch_app.models import EnergyData
from django.utils.timezone import make_aware

class Command(BaseCommand):
    help = 'Load energy data from hotel_energy_data.csv file into the database'

    def handle(self, *args, **kwargs):
        file_path = 'hotel_energy_data.csv' 

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            records=[]
            for row in reader:
                # Μετατροπή του timestamp σε datetime της python
                dt_unaware = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
                dt_aware = make_aware(dt_unaware) # Μετατροπή σε timezone-aware datetime
                
                # Cleaning
                solar_val=row['solar_kw'].strip()
                solar_clean=float(solar_val) if solar_val else 0.0
                load_val=row['load_kw'].strip()
                load_clean=float(load_val) if load_val else 0.0
                grid_price_val=row['grid_price_eur_per_kwh'].strip()
                grid_price_clean=float(grid_price_val) if grid_price_val else 0.0

                record = EnergyData(
                    timestamp=dt_aware,
                    solar_kw=solar_clean,
                    load_kw=load_clean,
                    grid_price_eur_per_kwh=grid_price_clean
                )
                records.append(record)
            
            EnergyData.objects.all().delete() # Διαγραφή όλων των προηγούμενων δεδομένων για να μην έχουμε διπλότυπα
            EnergyData.objects.bulk_create(records) # Εισαγωγή όλων των νέων δεδομένων με μία εντολή
        self.stdout.write(self.style.SUCCESS(f'Success! {len(records)} 15-mins records loaded.'))
