# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *
from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'main/index.html')

def process(request):
    errors = User.objects.validator(request.POST)
    if errors:
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/')
    else:
        hashed_pw = hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name=request.POST['name'], username=request.POST['username'],password=hashed_pw, date_hired=request.POST['hire_date'])
        request.session['id'] = user.id
        request.session['name']= user.name
        return redirect('/dashboard')

def login(request):
    login_return = User.objects.login(request.POST)
    if 'user' in login_return:
        request.session['id'] = login_return['user'].id
        request.session['name']= login_return['user'].name
        return redirect('/dashboard')
    else:
        messages.error(request, login_return['errors'])
        return redirect('/')

def dashboard(request):
    try:
        request.session['id']
    except KeyError:
        return redirect('/')

    user = User.objects.get(id=request.session['id'])
    context = {
        # 'myitem': User.objects.filter(id=request.session['id']).all(),
        'myitem': Item.objects.filter(added_by=user).all(),
        "addeditem": Item.objects.filter(all_items=user).all(),
        'mylist': Item.objects.exclude(added_by=user).exclude(all_items=user).all(),

    }
    return render(request, 'main/dashboard.html', context)

def display(request, item_id): 
    context = {
        'wishlist': Item.objects.filter(id=item_id).all(),
        'users': User.objects.filter(wishlists=item_id).all()
    }
    return render(request, 'main/display.html', context)

def add(request, item_id):
    a = Item.objects.get(id=item_id)
    User.objects.get(id=request.session['id']).wishlists.add(a)
    return redirect('/dashboard')

def remove(request, item_id):
    a = Item.objects.get(id=item_id)
    User.objects.get(id=request.session['id']).wishlists.remove(a)
    return redirect('/dashboard')
    #if statement for if created_by = session id, then you can remove, else you need to delete? 

def delete(request, item_id):
    a = Item.objects.get(id=item_id)
    a.delete()
    return redirect('/dashboard')

    # a.delete()
    # return redirect('/dashboard')

def addpage(request):
    return render(request, 'main/create.html')

def create(request):
    i_errors = Item.objects.item_validator(request.POST)
    if i_errors:
        for error in i_errors:
            messages.error(request, i_errors[error])
        return redirect('/addpage')
    else:
        item = Item.objects.create(item_name=request.POST['item_name'],added_by=User.objects.get(id=request.session['id']))
        return redirect('/dashboard')


def logout(request):
    del request.session
    return redirect('/')
