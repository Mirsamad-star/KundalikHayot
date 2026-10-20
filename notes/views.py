from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Note

@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user)
    return render(request, 'notes/list.html', {'notes': notes})

@login_required
def note_create(request):
    if request.method == 'POST':
        note = Note(
            user=request.user,
            title=request.POST.get('title', ''),
            content=request.POST.get('content', ''),
            is_pinned=request.POST.get('is_pinned') == 'on',
            color=request.POST.get('color', '#fef3c7'),
        )
        if 'attachment' in request.FILES:
            note.attachment = request.FILES['attachment']
        note.save()
        messages.success(request, 'Note created!')
        return redirect('note_list')
    return render(request, 'notes/form.html', {'action': 'Create'})

@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.title = request.POST.get('title', note.title)
        note.content = request.POST.get('content', '')
        note.is_pinned = request.POST.get('is_pinned') == 'on'
        note.color = request.POST.get('color', note.color)
        if 'attachment' in request.FILES:
            note.attachment = request.FILES['attachment']
        note.save()
        messages.success(request, 'Note updated!')
        return redirect('note_list')
    return render(request, 'notes/form.html', {'note': note, 'action': 'Edit'})

@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted!')
        return redirect('note_list')
    return render(request, 'notes/confirm_delete.html', {'note': note})
