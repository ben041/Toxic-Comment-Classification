from django.urls import path 
from . import views

urlpatterns = [
    path("AI-Engine/", views.engine_view, name="engine_view"),
    path('Word by word Analysis/', views.word_by_word, name='word_by_word'),
    path('About/', views.about, name='about'),
    path('Welcome/', views.landing_page, name='landing_page'),

    path('Real-time Analysis/', views.realtime_view, name='realtime'),
    path('analyze_text/', views.analyze_text, name='analyze_text'),

    path('', views.login_view, name='login'),
    path('Create an Account/', views.register_view, name='register'),
    path('Logout/', views.logout_view, name='logout'),
]
