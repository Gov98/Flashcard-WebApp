from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_category/', views.create_category, name='create_category'),
    path('create_card/', views.create_card, name='create_card'),
    path('manage_cards/', views.manage_cards, name='manage_cards'),
    path('view_category/<int:category_id>/', views.view_category, name='view_category'),
    path('update_card/<int:category_id>/<int:card_id>/', views.update_card, name='update_card'),
    path('learning/', views.learning, name='learning'),
    path('study_flashcards/<int:category_id>/', views.study_flashcards, name='study_flashcards'),
    path('get_interesting_facts/', views.get_interesting_facts, name='get_interesting_facts'),
    path('mark_correct_guess/', views.mark_correct_guess, name='mark_correct_guess'),
    path('category/<int:category_id>/card/<int:card_id>/', views.view_card, name='view_card'),
    path('submit_score/', views.submit_score, name='submit_score'),
    path('get_recent_score/', views.get_recent_score, name='get_recent_score'),  # Endpoint for fetching recent score
    path('get_deck_count/', views.get_deck_count, name='get_deck_count')
]
