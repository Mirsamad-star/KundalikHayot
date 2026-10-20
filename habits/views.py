from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Habit, HabitLog

@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user)
    today = timezone.now().date()
    logs_today = {
        log.habit_id: log
        for log in HabitLog.objects.filter(habit__user=request.user, date=today, completed=True)
    }
    return render(request, 'habits/list.html', {
        'habits': habits,
        'logs_today': logs_today,
        'today': today,
    })

@login_required
def habit_create(request):
    if request.method == 'POST':
        Habit.objects.create(
            user=request.user,
            name=request.POST.get('name', ''),
            description=request.POST.get('description', ''),
            frequency=request.POST.get('frequency', 'daily'),
            target_count=int(request.POST.get('target_count', 1) or 1),
            color=request.POST.get('color', '#6366f1'),
        )
        messages.success(request, 'Habit created!')
        return redirect('habit_list')
    return render(request, 'habits/form.html', {'action': 'Create'})

@login_required
def habit_edit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        habit.name = request.POST.get('name', habit.name)
        habit.description = request.POST.get('description', '')
        habit.frequency = request.POST.get('frequency', habit.frequency)
        habit.target_count = int(request.POST.get('target_count', habit.target_count) or 1)
        habit.color = request.POST.get('color', habit.color)
        habit.save()
        messages.success(request, 'Habit updated!')
        return redirect('habit_list')
    return render(request, 'habits/form.html', {'habit': habit, 'action': 'Edit'})

@login_required
def habit_delete(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        habit.delete()
        messages.success(request, 'Habit deleted!')
        return redirect('habit_list')
    return render(request, 'habits/confirm_delete.html', {'habit': habit})

@login_required
def habit_toggle(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    today = timezone.now().date()
    log, created = HabitLog.objects.get_or_create(
        habit=habit, date=today, defaults={'completed': True}
    )
    if not created:
        log.completed = not log.completed
        log.save()
    return redirect('habit_list')
