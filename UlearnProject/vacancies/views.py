from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse


def index(request):
    return render(request, 'index.html')


def geography_view(request):
    return render(request, 'geography.html')


def all_statistics_view(request):
    available_years = [2015, 2016, 2017, 2018,
                       2019, 2020, 2021, 2022, 2023, 2024]
    year = request.GET.get('year', available_years[-1])
    try:
        year = int(year)
    except ValueError:
        year = available_years[-1]

    if year not in available_years:
        year = available_years[-1]

    template_path = f"tables/all_skills/top_skills_by_year/top_skills_{
        year}.html"

    context = {
        "available_years": available_years,
        "selected_year": year,
        "template_path": template_path,
    }
    return render(request, "all_statistics.html", context)


def demand_view(request):
    return render(request, 'demand.html')


def skills_view(request):
    return render(request, 'skills.html')


def last_vacancies_view(request):
    return render(request, 'last_vacancies.html')
