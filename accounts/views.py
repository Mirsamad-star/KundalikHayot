from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task
from goals.models import Goal
from habits.models import Habit, HabitLog
from notes.models import Note
from expenses.models import Expense
from calendar_app.models import Event

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

@login_required
def dashboard(request):
    user = request.user
    today = timezone.now().date()
    
    # Stats
    tasks_todo = Task.objects.filter(user=user, status='todo').count()
    tasks_done = Task.objects.filter(user=user, status='done').count()
    active_goals = Goal.objects.filter(user=user, status='active').count()
    habits_count = Habit.objects.filter(user=user).count()
    notes_count = Note.objects.filter(user=user).count()
    
    # Recent
    recent_tasks = Task.objects.filter(user=user).order_by('-created_at')[:5]
    recent_notes = Note.objects.filter(user=user)[:5]
    upcoming_events = Event.objects.filter(user=user, start__gte=timezone.now()).order_by('start')[:5]
    
    # Habit logs today
    habits_today = HabitLog.objects.filter(habit__user=user, date=today, completed=True).count()
    
    # Expenses this month
    month_start = today.replace(day=1)
    month_expenses = Expense.objects.filter(
        user=user, type='expense', date__gte=month_start
    ).aggregate(total=Sum('amount'))['total'] or 0
    month_income = Expense.objects.filter(
        user=user, type='income', date__gte=month_start
    ).aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'tasks_todo': tasks_todo,
        'tasks_done': tasks_done,
        'active_goals': active_goals,
        'habits_count': habits_count,
        'notes_count': notes_count,
        'recent_tasks': recent_tasks,
        'recent_notes': recent_notes,
        'upcoming_events': upcoming_events,
        'habits_today': habits_today,
        'month_expenses': month_expenses,
        'month_income': month_income,
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def profile_view(request):
    if request.method == 'POST':
        profile = request.user.profile
        profile.bio = request.POST.get('bio', '')
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        profile.save()
        messages.success(request, 'Profile updated!')
        return redirect('profile')
    return render(request, 'accounts/profile.html')
