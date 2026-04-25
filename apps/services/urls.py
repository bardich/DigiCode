from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.ServiceListView.as_view(), name='list'),
    path('lp/rental/', views.RentalLandingPageView.as_view(), name='rental_landing'),
    path('<slug:slug>/', views.ServiceDetailView.as_view(), name='detail'),
]
