from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('set-language/<str:lang>/', views.SetLanguageView.as_view(), name='set_language'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('demos/cv-professionnel/', views.CVPortfolioDemoView.as_view(presentation='cv_professional'), name='cv_professional_demo'),
    path('demos/portfolio-creatif/', views.CVPortfolioDemoView.as_view(presentation='cv_creative'), name='cv_creative_demo'),
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
]
