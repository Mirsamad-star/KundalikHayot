from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task

@login_required
def task_list(request):
    status_filter = request.GET.get('status', '')
    tasks = Task.objects.filter(user=request.user)
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    return render(request, 'tasks/list.html', {'tasks': tasks, 'status_filter': status_filter})

@login_required
def task_create(request):
    if request.method == 'POST':
        task = Task(
            user=request.user,
            title=request.POST.get('title', ''),
            description=request.POST.get('description', ''),
            priority=request.POST.get('priority', 'medium'),
            status=request.POST.get('status', 'todo'),
            due_date=request.POST.get('due_date') or None,
        )
        if 'attachment' in request.FILES:
            task.attachment = request.FILES['attachment']
        task.save()
        messages.success(request, 'Task created!')
        return redirect('task_list')
    return render(request, 'tasks/form.html', {'action': 'Create'})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.title = request.POST.get('title', task.title)
        task.description = request.POST.get('description', '')
        task.priority = request.POST.get('priority', task.priority)
        task.status = request.POST.get('status', task.status)
        task.due_date = request.POST.get('due_date') or None
        if 'attachment' in request.FILES:
            task.attachment = request.FILES['attachment']
        task.save()
        messages.success(request, 'Task updated!')
        return redirect('task_list')
    return render(request, 'tasks/form.html', {'task': task, 'action': 'Edit'})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted!')
        return redirect('task_list')
    return render(request, 'tasks/confirm_delete.html', {'task': task})

@login_required
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if task.status == 'done':
        task.status = 'todo'
    else:
        task.status = 'done'
    task.save()
    return redirect('task_list')
