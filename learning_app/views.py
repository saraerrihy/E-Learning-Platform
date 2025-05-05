from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileEditForm

@login_required
def profile_view(request):
    user = request.user
    enrolled_courses = user.courses_joined.all()
    return render(request, 'learning_app/profile.html', {
        'user': user,
        'enrolled_courses': enrolled_courses
    })

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('learning_app:profile')
    else:
        form = ProfileEditForm(instance=request.user)
    
    return render(request, 'learning_app/profile_edit.html', {
        'form': form
    }) 