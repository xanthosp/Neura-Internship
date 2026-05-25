from django.contrib import admin
from django.urls import path
from dispatch_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reports/weekly/', views.weekly_report, name='weekly_report'),
]
