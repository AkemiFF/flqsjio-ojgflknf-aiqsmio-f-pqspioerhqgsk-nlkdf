from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Event, Participant
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Event
from .forms import EventForm
from messagerie.models import Message  # Modèle pour les messages
from django.contrib import messages
from django.contrib.auth.models import User

@login_required
def register_to_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if event.capacity > event.participants.count():
        Participant.objects.create(user=request.user, event=event)
    return redirect('event_detail', event_id=event.id)

@login_required
def unregister_from_event(request, event_id):
    Participant.objects.filter(user=request.user, event__id=event_id).delete()
    return redirect('event_detail', event_id=event_id)


class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('actu')

def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

def register_to_event(request, event_id):
    if request.method == "POST":
        event = get_object_or_404(Event, id=event_id)
        if event.capacity > event.participants.count():  # Vérifie si des places sont disponibles
            Participant.objects.get_or_create(user=request.user, event=event)  # Ajoute le participant
        return redirect('actu')
    


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from events.models import Event
from messagerie.models import Message  # Modèle pour les messages

@login_required
def share_event(request, event_id):
    # Exclure l'utilisateur connecté de la liste des destinataires possibles
    users = User.objects.exclude(id=request.user.id)
    # Récupérer l'événement à partager ou lever une 404 s'il n'existe pas
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        # Récupérer l'ID du destinataire et le contenu du message
        receiver_id = request.POST.get('receiver')
        message_content = request.POST.get('message')

        if receiver_id and message_content:
            # Vérifier si le destinataire existe
            receiver = get_object_or_404(User, id=receiver_id)

            # Créer un nouveau message dans la base de données
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                content=message_content  # Pas de chiffrement, enregistrement direct
            )

            # Ajouter une notification de succès
            messages.success(request, f"L'événement '{event.title}' a été partagé avec {receiver.username}!")
            return redirect('event_list')

        # Afficher un message d'erreur si les champs sont incomplets
        messages.error(request, 'Veuillez sélectionner un destinataire et écrire un message.')

    # Rendre le formulaire de partage avec la liste des utilisateurs et l'événement
    return render(request, 'messagerie/share_event.html', {'users': users, 'event': event})
