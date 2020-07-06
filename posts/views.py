from django.shortcuts import render
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import User
from accounts.models import Family
from .models import Post


@login_required
def add_image(request, id):
    """
    Show Image Share Form
    """
    user = request.user
    family = Family.objects.get(id=id)
    if family:
        # in case user messes with url to try to post to a wall they don't belong to
        if user not in family.get_members():
            messages.warning(request, "You do not have permission to and an image to this wall.")
            return redirect(reverse('wall'))
    else:
        # in case user bookmarks a page and db re-indexes
        messages.warning(request, "Sorry the family you are adding an image to does not exist.")
        return redirect(reverse('wall'))

    return render(request, "share_image.html")


@login_required
def update_image(request, id):
    """
    Show Image Update Form
    """
    user = request.user
    post = Post.objects.filter(id=id)
    if user != post.user:
        messages.warning(request, "You do not have permission to update this image")
        return redirect(reverse('wall'))

    return render(request, "update_image.html")


@login_required
def add_post(request, id):
    """
    Show Add Post Form
    """
    user = request.user
    family = Family.objects.get(id=id)
    if family:
        # in case user messes with url to try to post to a wall they don't belong to
        if user not in family.get_members():
            messages.warning(request, "You do not have permission to post to this wall.")
            return redirect(reverse('wall'))
    else:
        # in case user bookmarks a page and db re-indexes
        messages.warning(request, "Sorry the family you are posting to does not exist.")
        return redirect(reverse('wall'))

    return render(request, "create_post.html")


@login_required
def update_post(request, id):
    """
    Show Update Post Form
    """
    user = request.user
    post = Post.objects.filter(id=id)
    if user != post.user:
        messages.warning(request, "You do not have permission to update this post")
        return redirect(reverse('wall'))

    return render(request, "update_post.html")