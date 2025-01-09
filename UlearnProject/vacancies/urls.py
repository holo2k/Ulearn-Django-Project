from django.urls import path
from . import views

urlpatterns = [
    path('geography/', views.geography_view, name='geography'),
    path('all_statistics/', views.all_statistics_view, name='all_statistics'),
    path('demand/', views.demand_view, name='demand'),
    path('skills/', views.skills_view, name='skills'),
    path('last_vacancies/', views.last_vacancies_view, name='last_vacancies'),
]
