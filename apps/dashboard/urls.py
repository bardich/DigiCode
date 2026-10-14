from django.urls import path
from . import views, marketing_views

app_name = 'dashboard'

urlpatterns = [
    path('marketing/', marketing_views.MarketingListView.as_view(), name='marketing_list'),
    path('marketing/create/', marketing_views.MarketingCreateView.as_view(), name='marketing_create'),
    path('marketing/<int:pk>/edit/', marketing_views.MarketingUpdateView.as_view(), name='marketing_edit'),
    path('marketing/<int:pk>/delete/', marketing_views.MarketingDeleteView.as_view(), name='marketing_delete'),
    path('marketing/<int:pk>/toggle/', marketing_views.MarketingToggleView.as_view(), name='marketing_toggle'),
    path('marketing/switch/', marketing_views.MarketingGlobalView.as_view(), name='marketing_global'),
    path('inquiries/', views.InquiryListView.as_view(), name='inquiry_list'),
    path('inquiries/<int:pk>/', views.InquiryUpdateView.as_view(), name='inquiry_detail'),
    path('login/', views.DashboardLoginView.as_view(), name='login'),
    path('logout/', views.DashboardLogoutView.as_view(), name='logout'),
    path('', views.DashboardView.as_view(), name='index'),
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/create/', views.ServiceCreateView.as_view(), name='service_create'),
    path('services/<int:pk>/edit/', views.ServiceUpdateView.as_view(), name='service_edit'),
    path('services/<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='service_delete'),
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='project_edit'),
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
]
