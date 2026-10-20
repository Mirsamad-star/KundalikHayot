from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Goal

@login_required
def goal_list(request):
    goals = Goal.objects.filter(user=request.user)
    return render(request, 'goals/list.html', {'goals': goals})

@login_required
def goal_create(request):
    if request.method == 'POST':
        goal = Goal(
            user=request.user,
            title=request.POST.get('title', ''),
            description=request.POST.get('description', ''),
            target_date=request.POST.get('target_date') or None,
            status=request.POST.get('status', 'active'),
            progress=int(request.POST.get('progress', 0) or 0),
        )
        if 'image' in request.FILES:
            goal.image = request.FILES['image']
        goal.save()
        messages.success(request, 'Goal created!')
        return redirect('goal_list')
    return render(request, 'goals/form.html', {'action': 'Create'})

@login_required
def goal_edit(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        goal.title = request.POST.get('title', goal.title)
        goal.description = request.POST.get('description', '')
        goal.target_date = request.POST.get('target_date') or None
        goal.status = request.POST.get('status', goal.status)
        goal.progress = int(request.POST.get('progress', goal.progress) or 0)
        if 'image' in request.FILES:
            goal.image = request.FILES['image']
        goal.save()
        messages.success(request, 'Goal updated!')
        return redirect('goal_list')
    return render(request, 'goals/form.html', {'goal': goal, 'action': 'Edit'})

@login_required
def goal_delete(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        goal.delete()
        messages.success(request, 'Goal deleted!')
        return redirect('goal_list')
    return render(request, 'goals/confirm_delete.html', {'goal': goal})
