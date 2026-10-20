from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .models import Event

@login_required
def event_list(request):
    events = Event.objects.filter(user=request.user)
    return render(request, 'calendar_app/list.html', {'events': events})

@login_required
def event_create(request):
    if request.method == 'POST':
        start_str = request.POST.get('start')
        end_str = request.POST.get('end') or None
        Event.objects.create(
            user=request.user,
            title=request.POST.get('title', ''),
            description=request.POST.get('description', ''),
            start=start_str,
            end=end_str,
            all_day=request.POST.get('all_day') == 'on',
            location=request.POST.get('location', ''),
            color=request.POST.get('color', '#3b82f6'),
        )
        messages.success(request, 'Event created!')
        return redirect('event_list')
    return render(request, 'calendar_app/form.html', {'action': 'Create'})

@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)
    if request.method == 'POST':
        event.title = request.POST.get('title', event.title)
        event.description = request.POST.get('description', '')
        event.start = request.POST.get('start') or event.start
        event.end = request.POST.get('end') or None
        event.all_day = request.POST.get('all_day') == 'on'
        event.location = request.POST.get('location', '')
        event.color = request.POST.get('color', event.color)
        event.save()
        messages.success(request, 'Event updated!')
        return redirect('event_list')
    return render(request, 'calendar_app/form.html', {'event': event, 'action': 'Edit'})

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted!')
        return redirect('event_list')
    return render(request, 'calendar_app/confirm_delete.html', {'event': event})
