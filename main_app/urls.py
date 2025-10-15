from django.urls import path
from . import views
from .views import SignUpView, CustomLoginView, CustomLogoutView



urlpatterns = [

    path('', views.homepage, name='homepage'),
    path('cars/', views.cars_list, name='cars_list'),
    path('cars/<int:car_id>/book/', views.book_car, name='book_car'),
    path('requests/', views.requests_list, name='requests_list'),
    path('cars/create/', views.add_car, name='add_car'),
    path('requests/<int:request_id>/<str:action>/', views.request_action, name='request_action'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('requests/clear/', views.clear_requests, name='clear_requests'),

]
