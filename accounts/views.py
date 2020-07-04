from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from accounts.forms import UserLoginForm, UserRegistrationFrom, CreateFamilyForm
from .models import Family
import json
from .password import random_string


@login_required
def logout(request):
    """Log the user out"""
    auth.logout(request)
    messages.success(request, 'You have successfully been logged out.')
    return redirect(reverse('index'))


def login(request):
    """Render login page"""
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])

            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully logged in")
                return redirect(reverse('index'))
            else:
                login_form.add_error(None, "Username/email and password not valid.")
    else:
        login_form = UserLoginForm()

    return render(request, 'login.html', {"login_form": login_form})


def registration(request):
    """Render the registration page"""
    if request.user.is_authenticated:
        # logged in users can't go to registration page, send them back to challenges page
        messages.error(request, 'You are already a registered user.')
        return redirect(reverse('index'))

    if request.method == "POST":
        registration_form = UserRegistrationFrom(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully registered.")
                return redirect(reverse('index'))
            else:
                messages.error(request, 'Unable to register your account at this time')

    else:
        registration_form = UserRegistrationFrom()

    return render(request, 'registration.html', {"registration_form": registration_form})


@login_required
def default_wall(request):
    """
    Display fisrt wall in user's list. User must be authenticated to get here.
    """
    user = User.objects.get(pk=request.user.pk)
    family = Family.objects.filter(members=user).first()

    if family:
        return render(request, "walls/wall.html", {"family": family, "user": user})
    else:
        messages.success(request, "You do not belong to any families yet, please create one.")
        return redirect(reverse('create_family'))


@login_required
def wall(request, id):
    """
    Display uesr's desired wall. User must be authenticated to get here.
    """
    user = request.user
    family = Family.objects.get(pk=id)
    members = family.members
    if user not in members:
        messages.warning(request, "I'm sorry, you do not belong to the family selected.")

    if family:
        return render(request, "walls/wall.html", {"family": family, "user": user})
    else:
        messages.success(request, "You do not belong to any families yet, please create one.")
        return redirect(reverse('create_family'))


@login_required
def create_family(request):
    """
    Create Family page
    """
    user = request.user
    form = CreateFamilyForm(initial={'members': [user.email]})
    if request.method == 'POST':
        form = CreateFamilyForm(request.POST, request.FILES)
        if 'cancel' in request.POST:
            return redirect(reverse('default_wall'))
        if form.is_valid():
            family = Family.objects.create(
                family_name=form.cleaned_data['family_name'],
                hero_image=request.FILES['hero_image'],
            )
            family.save()
            try:
                members = json.loads(form.data['members'])
            except:
                members = [{'email': user.email}]
            member_status = []
            for member in members:
                user1 = User.objects.filter(email=member['email']).first()
                if user1:
                    user1 = user1
                    family.members.add(user1)
                    member_status.append({
                        'user': user1.pk,
                        'status': 'existing',
                    })
                else:
                    # create a user
                    passwd = random_string(4, 4)
                    user1 = User.objects.create(
                        email=member['email'],
                        username=member['email'],
                        password=passwd,
                        first_name=member['first_name'],
                        last_name=member['last_name'],
                    )

                    family.members.add(user1)
                    member_status.append({
                        'user': user1.pk,
                        'status': 'new',
                    })

                    # TODO send email to users inviting them to the family
                    # initial_email(member_status, challenge)

            # let user know the challenge was created
            messages.success(request,
                             "Your family: " + family.family_name.title() + " was successfully created and an invite has been sent to the members.")

            return redirect('wall', family.pk)
            # return render(request, "wall.html", {"family": family, "user": user})
    return render(request, "walls/create_family.html", {"form": form, })
