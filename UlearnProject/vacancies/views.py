from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .scripts.get_vacancies import run
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout


class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'profile.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    return redirect('../accounts/login')


def logout_view(request):
    logout(request)
    return redirect('../accounts/login')


@login_required
def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    return redirect('login')


@login_required
def geography_view(request):
    return render(request, 'geography.html')


@login_required
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


@login_required
def demand_view(request):
    return render(request, 'demand.html')


@login_required
def skills_view(request):
    available_years = [2015, 2016, 2017, 2018,
                       2019, 2020, 2021, 2022, 2023, 2024]
    year = request.GET.get('year', available_years[-1])
    try:
        year = int(year)
    except ValueError:
        year = available_years[-1]

    if year not in available_years:
        year = available_years[-1]

    template_path = f"tables/sharp_skills/top_skills_by_year/top_skills_{
        year}.html"

    context = {
        "available_years": available_years,
        "selected_year": year,
        "template_path": template_path,
    }
    return render(request, "skills.html", context)


@login_required
def last_vacancies_view(request):
    vacancies = run()
    return render(request, 'last_vacancies.html', {'vacancies': vacancies})
