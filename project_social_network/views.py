from django.shortcuts import render
from django.http import HttpResponse

from .models import Member, Profile

appname = 'Social network for billiard players'


def index(request):
    return render(request, 'index.html', {
        'appname': appname
    })


def signup(request):
    return render(request, 'signup.html', {
        'appname': appname
    })


def register(request):
    entered_user = request.POST['user']
    entered_password = request.POST['pass']
    try:
        member = Member.objects.get(pk=entered_user)
    except Member.DoesNotExist:
        member = None

    if member is None:
        user = Member(username=entered_user, password=entered_password)
        user.save()
        return render(request, 'user-registered.html', {
            'appname': appname,
            'username': entered_user
        })
    else:
        return render(request, 'signup.html', {
            'appname': appname,
            'username': entered_user,
            'error': "User already exists!"
        })


def login(request):
    if 'username' not in request.POST:
        return render(request, 'login.html', {
            'appname': appname
        })
    else:
        entered_username = request.POST['username']
        entered_password = request.POST['password']
        try:
            member = Member.objects.get(pk=entered_username)
        except Member.DoesNotExist:
            return render(request, 'login.html', {
                'appname': appname,
                'error': "User does not exist"
            })
        if member.password == entered_password:
            request.session['username'] = entered_username
            request.session['password'] = entered_password
            return render(request, 'login.html', {
                'appname': appname,
                'username': entered_username,
                'loggedin': True}
                          )
        else:
            return render(request, 'login.html', {
                'appname': appname,
                'error': "Incorrect username or password"
            })


def logout(request):
    if 'username' in request.session:
        current_username = request.session['username']
        request.session.flush()
        return render(request, 'logout.html', {
            'appname': appname,
            'username': current_username
        })
    else:
        return render(request, 'index.html', {
            'appname': appname,
            'error': "You are not logged in"
        })


def member(request, view_user):
    if 'username' in request.session:
        username = request.session['username']
        member = Member.objects.get(pk=view_user)

        if view_user == username:
            greeting = "Your"
        else:
            greeting = view_user + "'s"

        if member.profile:
            text = member.profile.text
        else:
            text = ""
        return render(request, 'member.html', {
            'appname': appname,
            'username': username,
            'greeting': greeting,
            'profile': text,
            'loggedin': True
        })
    else:
        return render(request, 'index.html', {
            'appname': appname,
            'error': "You are not logged in, no access to member page!"
        })


def profile(request):
    if 'username' in request.session:
        entered_username = request.session['username']
        member = Member.objects.get(pk=entered_username)

        if 'text' in request.POST:
            text = request.POST['text']
            if member.profile:
                member.profile.text = text
                member.profile.save()
            else:
                profile = Profile(text=text)
                profile.save()
                member.profile = profile
            member.save()
        else:
            if member.profile:
                text = member.profile.text
            else:
                text = ""
        return render(request, 'profile.html', {
            'appname': appname,
            'username': entered_username,
            'text': text,
            'loggedin': True}
                      )
    else:
        return render(request, 'index.html', {
            'appname': appname,
            'error': "You are not logged in, no access to profile page!"
        })


def member(request, view_user):
    if 'username' in request.session:
        username = request.session['username']
        member = Member.objects.get(pk=view_user)

        if view_user == username:
            greeting = "Your"
        else:
            greeting = view_user + "'s"

        if member.profile:
            text = member.profile.text
        else:
            text = ""
        return render(request, 'member.html', {
            'appname': appname,
            'username': username,
            'greeting': greeting,
            'profile': text,
            'loggedin': True
        })
    else:
        return render(request, 'index.html', {
            'appname': appname,
            'error': "You are not logged in, no access to member page!"
        })


def members(request):
    if 'username' in request.session:
        username = request.session['username']
        member_obj = Member.objects.get(pk=username)
        if 'add' in request.GET:
            friend = request.GET['add']
            friend_obj = Member.objects.get(pk=friend)
            member_obj.following.add(friend_obj)
            member_obj.save()
        if 'remove' in request.GET:
            friend = request.GET['remove']
            friend_obj = Member.objects.get(pk=friend)
            member_obj.following.remove(friend_obj)
            member_obj.save()
        if 'view' in request.GET:
            return member(request, request.GET['view'])
        else:
            members = Member.objects.exclude(pk=username)
            following = member_obj.following.all()
            followers = Member.objects.filter(following__username=username)
            return render(request, 'members.html', {
                'appname': appname,
                'username': username,
                'members': members,
                'following': following,
                'followers': followers,
                'loggedin': True}
                          )
    else:
        return render(request, 'index.html', {
            'appname': appname,
            'error': "You are not logged in!"
        })


def friends(request):
    if 'username' in request.session:
        username = request.session['username']
        member_obj = Member.objects.get(pk=username)
        following = member_obj.following.all()
        followers = Member.objects.filter(following__username=username)
        return render(request, 'friends.html', {
            'appname': appname,
            'username': username,
            'members': members,
            'following': following,
            'followers': followers,
            'loggedin': True}
                      )
    else:
        return render(request, 'index.html', {
            'appname': appname,
            'error': "You are not logged in!"
        })
