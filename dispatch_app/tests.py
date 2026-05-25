from django.test import TestCase

from django.test import TestCase
from .models import EnergyData
from .services import run_dispatch_simulation
from django.utils import timezone
from datetime import timedelta

class DispatchLogicTests(TestCase):
    def setUp(self):
        # Φτιάχνουμε 2 15-λεπτα records για να τεστάρουμε τον αλγόριθμο
        now = timezone.now()
        EnergyData.objects.create(
            timestamp=now, solar_kw=100.0, load_kw=50.0, grid_price_eur_per_kwh=0.30
        )
        EnergyData.objects.create(
            timestamp=now + timedelta(minutes=15), solar_kw=0.0, load_kw=100.0, grid_price_eur_per_kwh=0.30
        )

    def test_run_dispatch_simulation(self):
        # Τρέχουμε τον αλγόριθμο
        results = run_dispatch_simulation(battery_capacity_kwh=400.0)
        
        # Ελέγχουμε αν επέστρεψε 2 αποτελέσματα (όσα και τα records μας)
        self.assertEqual(len(results), 2)
        
        # Στο πρώτο 15-λεπτο (Πλεόνασμα ήλιου 50kW), η μπαταρία πρέπει να φορτίζει (αρνητικό πρόσημο)
        self.assertTrue(results[0]['battery_kw'] < 0)
        
        # Στο δεύτερο 15-λεπτο (Έλλειμμα 100kW μέρα), η μπαταρία πρέπει να εκφορτίζει (θετικό πρόσημο)
        self.assertTrue(results[1]['battery_kw'] > 0)