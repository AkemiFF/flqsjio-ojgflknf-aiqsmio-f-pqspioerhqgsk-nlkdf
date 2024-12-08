from django.contrib import admin
from .models import Event, Participant

# Configuration pour le modèle Event
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'capacity', 'organizer')  # Colonnes affichées
    search_fields = ('title', 'location')  # Champs de recherche
    list_filter = ('date',)  # Filtres dans la barre latérale
    ordering = ('-date',)  # Ordre par défaut
    autocomplete_fields = ['organizer']  # Auto-complétion pour les relations FK

# Configuration pour le modèle Participant
@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'registered_at')  # Colonnes affichées
    search_fields = ('user__username', 'event__title')  # Champs de recherche
    list_filter = ('registered_at',)  # Filtres dans la barre latérale
    ordering = ('-registered_at',)  # Ordre par défaut
