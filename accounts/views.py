from smtplib import SMTPResponseException

from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from accounts.forms import UserLoginForm, UserRegistrationFrom, CreateFamilyForm
from accounts.models import Family
from users.models import User
from .forms import ProfileForm
import json
from .password import random_string
from posts.models import Post
from ci_hackathon_july_2020.settings import EMAIL_HOST_USER, DEFAULT_DOMAIN
from django.core.mail import EmailMultiAlternatives, EmailMessage
import logging
from status.forms import MOOD_CHOICES

log = logging.getLogger(__name__)


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
            user = auth.authenticate(
                email=request.POST['email'], password=request.POST['password'])

            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully logged in")
                return redirect(reverse('index'))
            else:
                login_form.add_error(None, "Email and/or password not valid.")
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
            user = auth.authenticate(email=request.POST['email'],
                                     password=request.POST['password1'])

            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully registered.")
                return redirect(reverse('index'))
            else:
                messages.error(
                    request, 'Unable to register your account at this time')

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
        posts = Post.objects.filter(
            family=family.pk).order_by('-datetime')[:30]
        families = list(Family.objects.filter(members=user))
        if not posts:
            posts = []
        return render(request, "walls/wall.html",
                      {"family": family, "user": user, "posts": posts, "families": families,
                       "mood_choices": MOOD_CHOICES})
    else:
        messages.success(
            request, "You do not belong to any families yet, please create one.")
        return redirect(reverse('create_family'))


@login_required
def wall(request, id):
    """
    Display uesr's desired wall. User must be authenticated to get here.
    """
    user = request.user
    family = Family.objects.get(pk=id)
    members = family.get_members()
    if user not in members:
        messages.warning(
            request, "I'm sorry, you do not belong to the family selected.")

    if family:
        families = list(Family.objects.filter(members=user))
        posts = Post.objects.filter(
            family=family.pk).order_by('-datetime')[:30]
        if not posts:
            posts = []
        return render(request, "walls/wall.html",
                      {"family": family, "user": user, "posts": posts, "families": families,
                       "mood_choices": MOOD_CHOICES})
    else:
        messages.success(
            request, "You do not belong to any families yet, please create one.")
        return redirect(reverse('create_family'))


@login_required
def create_family(request):
    """
    Create Family page
    """
    user = request.user
    form = CreateFamilyForm()
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
                members.append({'email': user.email})
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
                        password=passwd,
                    )

                    family.members.add(user1)
                    member_status.append({
                        'user': user1.pk,
                        'status': 'new',
                    })

                    # send email to users inviting them to the family
                    initial_email(member_status, family)

            # let user know the challenge was created
            messages.success(request,
                             "Your family: " + family.family_name.title() + " was successfully created and an invite has been sent to the members.")

            return redirect('wall', family.pk)
            # return render(request, "wall.html", {"family": family, "user": user})
    return render(request, "walls/create_family.html", {"form": form, })


def initial_email(members, family):
    """
    Send email to users inviting them to the family wall
    """
    try:
        from_email = EMAIL_HOST_USER

        # new to Family Wall Welcome Email for auto created users, send them a welcome message with password [status=new]
        new_subject = "Welcome to The Family Wall!"
        new_msg_greeting = "Hello! \n\nYou have been declared a member of a family wall. Since you have not yet been invited to our forum, we have auto created an account for you. "
        new_closing = "\n\nDon't worry, you can change your email and password once you login. The details about the Family you've been invited to will follow shortly. Thank you and Have a Nice Day!"
        to = []
        # loop through members and build list of users to get Join a Family email and send of welcome message
        for member in members:
            user = User.objects.get(pk=member['user'])
            to.append(user.email)
            if member['status'] == "new":
                # if user is new, send them welcome email
                new_content1 = "Your email address: " + user.email + " is how you login. "
                new_content2 = "Your password is: " + user.password
                new_msg = new_msg_greeting + new_content1 + new_content2 + new_closing
                new_msg_html = "<p>" + new_msg_greeting + "</p>"
                new_msg_html += "<p>" + new_content1 + "</p>"
                new_msg_html += "<p>" + new_content2 + "</p>"
                new_msg_html += "<p>" + new_closing + "</p>"
                msg = EmailMultiAlternatives(
                    new_subject, new_msg, from_email, to)
                msg.attach_alternative(new_msg_html, "text/html")
                msg.send()

        # Build You've been added to a Challenge Email [status !=new, 'existing']
        subject = "Congrats! You've been added to " + \
            family.family_name.title() + " on Family Wall!"
        text_content = 'Hello!\n\nA Family Wall has been created and you were declared a member!'
        url_msg = "See what your family is up to at: " + DEFAULT_DOMAIN + "/accounts/get_family/" + str(
            family.pk) + "/ "
        text_content += url_msg
        html_content = '<div style="font-size: 16px; width:100%; margin: 20px;"><p>Hello!</p><p>A Family Wall has been created and you were declared a member!'

        if family.hero_image:
            html_content += "<div style='height: 150px; width: 320px; margin: 20px auto; display:inline-block; background: url(" + \
                family.hero_image.url + ");background-size:contain; background-repeat:no-repeat;'></div>"
        html_content += "<p>" + url_msg + "</p>"
        closing_msg = "Have Fun and Have a Nice Day!"

        text_content += "\n\n" + closing_msg
        html_content += "<p>" + closing_msg + "</p></div>"

        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except SMTPResponseException as e:
        error_code = e.smtp_code
        error_message = e.smtp_error
        log.warning(f"WARNING: STMPResponseException: ",
                    error_code, error_message)

    return True


@login_required
def userprofile(request):
    """
    Profile settings for the user,
    to change/update their own profile.
    """
    user = request.user
    form = ProfileForm(instance=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()

            messages.info(request, 'Profile updated successfully')
            context = {'form': form}
            return render(request, 'userprofile.html', context)
    else:
        context = {'form': form}
        return render(request, 'userprofile.html', context)
