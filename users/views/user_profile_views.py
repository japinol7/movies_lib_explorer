from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404


@login_required
def profile_listing(request):
    data = {
        'profiles': User.objects.filter(is_staff=False)
        }
    return render(request, 'users/profile_listing.html', data)


@login_required
def profile(request, profile_id):
    # Only staff can see staff profiles
    if request.user.is_authenticated and request.user.is_staff:
        user_profile = get_object_or_404(User, id=profile_id)
    else:
        user_profile = get_object_or_404(User, id=profile_id, is_staff=False)

    data = {
        'profile': user_profile,
        }
    return render(request, 'users/profile.html', data)
