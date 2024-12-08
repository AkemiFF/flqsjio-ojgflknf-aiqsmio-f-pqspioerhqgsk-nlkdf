from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.event_list, name='actu'),
    path('events/<int:event_id>/register/', views.register_to_event, name='register_to_event'),
    path('events/<int:event_id>/share/', views.share_event, name='share_event'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
]
