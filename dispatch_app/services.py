from .models import EnergyData

# Τρέχει τον Dispatch of battery for all the records in the database and returns a list of 15-min dictionaries
def run_dispatch_simulation(battery_capacity_kwh=400.0): # <-- ΑΛΛΑΓΗ 1: Παράμετρος
    records = EnergyData.objects.all().order_by('timestamp')

    # Battery parameters
    Capacity_kwh = float(battery_capacity_kwh) # <-- ΑΛΛΑΓΗ 2: Δυναμικό capacity
    Max_Power_kW = 200.0
    Min_SOC = 0.1 * Capacity_kwh
    Max_SOC = 0.95 * Capacity_kwh
    Rte = 0.88
    Step_hours = 0.25

    current_soc = Min_SOC
    results = []

    for r in records:
        solar=r.solar_kw
        load=r.load_kw
        price=r.grid_price_eur_per_kwh

        battery_kw = 0.0 # (+) για φόρτιση, (-) για εκφόρτιση
        curtailed_kw = 0.0
        grid_import_kw = 0.0

        net_load = load - solar
        if net_load < 0: # Πλεόνασμα, φορτίζουμε μπαταρία
            surplus = abs(net_load)
            space_kwh = Max_SOC - current_soc # Χώρος που έχει η μπαταρία για να φορτίσει
            space_kw = space_kwh / (Step_hours*Rte) # Space, με υπολογισμό των απωλειών φόρτισης
            charge_kw = min(surplus, Max_Power_kW, space_kw) 

            current_soc += charge_kw * Step_hours * Rte 
            battery_kw = -charge_kw # Αρνητικό για φόρτιση
            curtailed_kw = surplus - charge_kw # Το υπόλοιπο πλεόνασμα που δεν μπορούμε να αποθηκεύσουμε

        elif net_load > 0: # Έλλειμμα, χρειαζόμαστε ρεύμα
            if price == 0.30: # Ακριβό ρεύμα, εκφορτίζουμε
                avail_kwh = current_soc - Min_SOC
                avail_kw = avail_kwh / Step_hours

                discharge_kw = min(net_load, Max_Power_kW, avail_kw)
                current_soc -= discharge_kw * Step_hours
                battery_kw = discharge_kw # Θετικό για εκφόρτιση
                grid_import_kw = net_load - discharge_kw # Το υπόλοιπο που πρέπει να πάρουμε από το δίκτυο
            else: # Φτηνό ρεύμα, Στρατηγική: κραταμε το SoC, παίρνουμε φθηνά από το δίκτυο
                grid_import_kw = net_load
    
       
        cost_no_battery = max(0, load - solar) * price * Step_hours
        cost_with_battery = grid_import_kw * price * Step_hours

        results.append({
            'timestamp': r.timestamp,
            'load_kw': load,
            'solar_kw': solar,
            'grid_price': price,
            'net_load_kw': net_load, # Άλλαξα ελάχιστα το όνομα εδώ σε net_load_kw για να "κουμπώσει" με το views.py
            'battery_kw': battery_kw,
            'soc_percent': (current_soc / Capacity_kwh) * 100,
            'curtailed_kw': curtailed_kw,
            'grid_import_kw': grid_import_kw,
            'cost_no_battery': cost_no_battery,
            'cost_with_battery': cost_with_battery,
        })
        
    return results