# A comprehensive behind-the-meter battery dispatch simulation for a commercial hotel in Limassol, Cyprus, built as a Django web service.

## Local Setup

I build this using Python 3. 12 and SQLite. To run the simulation locally: 

1. **Clone this repository** to your local machine.
2. **Create and activate a virtual environment**:
   python -m venv env
   # Windows: .\env\Scripts\activate
   # Mac/Linux: source env/bin/activate
3. **Install dependencies**:
    pip install -r requirements.txt
4. **Load the initial data into the SQLite database**:
    python manage.py load_data
5. **Start the Django development server**: 
    python manage.py runserver
6. **Open your browser and navigate to the weekly report dashboard**:
    http://127.0.0.1:8000/reports/weekly/

The Django Challenge:
My background is heavily focused on data, algorithms, and lower-level programming. Building a web service with Django was a completely new experience for me. However, I can say that with the help of AI (Gemini), I was able to quickly grasp the whole Django structure (urls.py, views.py, etc.) and navigate the local server environment. It also acted as a great pair-programmer for debugging server errors. Setting up the framework was arguably the most challenging aspect of the project, taking up about an hour, but it allowed me to focus the rest of my time on the core logic.

Dispatch algorithm:
I implemented a greedy policy with one specific strategic assumption:
1. Surplus Solar: Charge the battery up to the 200KW limit(accounting for 88% RTE). Curtailed the rest.
2. Peak Hours(€0.3): Dispatch the battery to cover the net load.
3. Off-peak Hours(€0.15): I chose not to discharge the battery overnight to cover the base load. Instead, we pull from the cheap grid. This preserves the SoC space to soak up the free morning solar and saves the battery's energy for the most expencive afternoon peak.

What i would build next:
1. Integrated Forecasting (Weather & Prices): The current algorithm is reactive. To achieve truly optimal savings, I would integrate next-day forecasting for both weather conditions (solar generation) and electricity prices. This would set decisive bounds for an advanced dispatch algorithm, moving beyond a simple greedy approach.

2. Real-world Data of Limassol: A static synthetic load isn't enough for the real world. I would analyze the hotel's actual consumption patterns on an hourly and monthly basis. Having precise, real-world data across seasons is crucial for the optimal operation of the battery.

3. Business Optimization Analysis: I would expand the tool to analyze the financial viability of different hardware setups. For instance, simulating if adding more PV panels or changing the battery specifications would yield a better Return on Investment (ROI) and minimize overall costs.