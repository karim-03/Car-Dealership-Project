from django.shortcuts import render, redirect
from .models import Cars, CustomUser, Requests
from django.urls import reverse, reverse_lazy
from .forms import CustomUserCreationForm, CarsForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST




def homepage(request):
    all_users = CustomUser.objects.all()
    return render(request, 'homepage.html', {'all_users': all_users})


def cars_list(request):
    form = CarsForm()
    available_cars = Cars.objects.filter(status__iexact='available')
    return render(request, 'lists/cars_list.html', {'form': form, 'all_cars': available_cars})

def add_car(request):
    if not request.user.is_authenticated:
        messages.info(request, "You need to be signed in to add a car.")
        return redirect('cars_list')

    if request.method == 'POST':
        form = CarsForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.seller = request.user.username
            car.save()
            messages.success(request, "Your car was added to the listing.")
            return redirect('cars_list')
    else:
        form = CarsForm()
    return render(request, 'lists/add_car.html', {'form': form})


@login_required
def book_car(request, car_id):
    car = Cars.objects.get(pk=car_id)
    if car.status.lower() != 'available':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'not available'}, status=400)
        return redirect(reverse('cars_list'))

    new_request = Requests.objects.create(user_id=request.user, car_id=car, status='pending')
    car.status = 'pending'
    car.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'request_id': new_request.id,
            'car_id': car.id,
            'status': new_request.status,
        })

    return redirect(reverse('requests_list') if _is_admin(request.user) else reverse('cars_list'))


def _is_admin(user):
    return user.is_authenticated and user.role == 'Admin'


@user_passes_test(_is_admin)
def requests_list(request):
    all_requests = Requests.objects.all()
    return render(request, 'lists/requests.html', {'all_requests': all_requests})


@user_passes_test(_is_admin)
def request_action(request, request_id, action):
    if request.method != 'POST':
        return HttpResponseBadRequest('POST required')
    try:
        req = Requests.objects.get(pk=request_id)
    except Requests.DoesNotExist:
        return JsonResponse({'error': 'request not found'}, status=404)

    if action not in ('accept', 'deny'):
        return JsonResponse({'error': 'invalid action'}, status=400)

    car = req.car_id
    if action == 'accept':
        req.status = 'accepted'
        car.status = 'sold'
    else:
        req.status = 'denied'
        car.status = 'available'

    req.save()
    car.save()
    return JsonResponse({'request_id': req.id, 'status': req.status, 'car_id': car.id})


@user_passes_test(_is_admin)
@require_POST
def clear_requests(request):
    from .models import Requests
    Requests.objects.all().delete()
    messages.success(request, "All requests have been cleared.")
    return redirect("requests_list")


def all_users(request):
    all_users = CustomUser.objects.all()
    return render(request, 'homepage.html', {'users': all_users})

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

