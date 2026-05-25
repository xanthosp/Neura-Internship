from django.db import models

class EnergyData(models.Model):
    timestamp = models.DateTimeField(unique=True, help_text="15-minute interval timestamp")
    solar_kw = models.FloatField(help_text="PV production in kW")
    load_kw = models.FloatField(help_text="Hotel demand in kW")
    grid_price_eur_per_kwh = models.FloatField(help_text="Grid price in EUR/kWh")

    class Meta:
        ordering = ['timestamp'] # Φροντίζει τα δεδομένα να έρχονται πάντα με χρονολογική σειρά

    def __str__(self):
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M')} | Load: {self.load_kw:.1f}kW | Solar: {self.solar_kw:.1f}kW"
