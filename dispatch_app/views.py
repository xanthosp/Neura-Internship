from django.shortcuts import render
from .services import run_dispatch_simulation

def weekly_report(request):
    # Διαβάζουμε το μέγεθος της μπαταρίας από το URL
    user_capacity = request.GET.get('capacity', 400)
    try:
        capacity_float = float(user_capacity)
        if capacity_float <= 0:
            capacity_float = 400.0 # Αποτροπή μηδενικής μπαταρίας 
    except ValueError:
        capacity_float = 400.0

    # Τρέχουμε τον αλγόριθμο
    dispatch_results = run_dispatch_simulation(battery_capacity_kwh=capacity_float)

    total_grid_spend_no_battery = 0
    total_grid_spend_with_battery = 0
    total_charged_kwh = 0
    total_discharged_kwh = 0
    total_solar_kwh = 0
    total_curtailed_kwh = 0
    labels = []
    soc_data = []

    for r in dispatch_results:
        total_grid_spend_no_battery += r['cost_no_battery']
        total_grid_spend_with_battery += r['cost_with_battery']
        total_solar_kwh += r['solar_kw'] * 0.25
        total_curtailed_kwh += r['curtailed_kw'] * 0.25

        if r['battery_kw'] < 0:
            total_charged_kwh += abs(r['battery_kw']) * 0.25
        elif r['battery_kw'] > 0:
            total_discharged_kwh += r['battery_kw'] * 0.25

        labels.append(r['timestamp'].strftime('%a %H:%M'))
        soc_data.append(round(r['soc_percent'], 1))

    savings = total_grid_spend_no_battery - total_grid_spend_with_battery
    used_solar = total_solar_kwh - total_curtailed_kwh
    
   
    if total_solar_kwh > 0:
        self_consumption_pct = (used_solar / total_solar_kwh) * 100
    else:
        self_consumption_pct = 0

    # Extra, calculation of ROI for the battery investment
    estimated_capex = capacity_float * 300
    # ~17 weeks of summer + 35 weeks with ~40% of savings at other times of the year
    annual_savings = (savings * 17) + (savings*0.40*35)
    
    if annual_savings > 0:
        base_roi_years = estimated_capex / annual_savings
        estimated_roi_years = base_roi_years * 1.05 # +5% degration penalty
    else:
        estimated_roi_years = 0

    context = {
        'current_capacity': capacity_float,
        'total_grid_spend_no_battery': round(total_grid_spend_no_battery, 2),
        'total_grid_spend_with_battery': round(total_grid_spend_with_battery, 2),
        'savings': round(savings, 2),
        'total_charged_kwh': round(total_charged_kwh, 2),
        'total_discharged_kwh': round(total_discharged_kwh, 2),
        'self_consumption_pct': round(self_consumption_pct, 1),
        'estimated_roi_years': round(estimated_roi_years, 1),
        'labels': labels,
        'soc_data': soc_data,
    }

    return render(request, 'dispatch_app/weekly_report.html', context)