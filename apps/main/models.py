# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt


class ItemManager(models.Manager):
    def item_validator(self, postData): 
        i_errors = {}
        if len(postData['item_name']) < 1:
            i_errors['empty'] = "Cannot add empty field"
        if len(postData['item_name']) < 3  or len(postData['item_name']) < 1:
            i_errors['len'] = "Item must be 3 characters or more"
        if Item.objects.filter(item_name=postData['item_name']):
            i_errors['exists'] = "Item already exists"
        return i_errors

class UserManager(models.Manager):
    def validator(self, postData): 
        errors ={}
        if len(postData['name']) < 3:
            errors['name_error'] = "Name must be 3 characters or more"
        if len(postData['username']) < 3:
            errors['user_error'] = "Username must be 3 characters or more"
        if len(postData['password']) < 8:
            errors['pass_len'] = "*Passwords must be 8 characters or more"
        if postData['password'] != postData['confirm_password']:
            errors['pass_match'] = "Passwords do not match"
        if User.objects.filter(username=postData['username']):
            errors['exists'] = "Username has already been taken"
        return errors
       
    def login(self, postData):
        user_check = User.objects.filter(username=postData['username'])
        if len(user_check) > 0:
            user_check = user_check[0] 
            if bcrypt.checkpw(postData['password'].encode(), user_check.password.encode()):
                user = {'user': user_check} 
                return user
            else:
                errors = {'errors': "Invalid Login. Please try again"}
                return errors
        else:
            errors = {'errors': "Invalid Login. Please try again"}
            return errors



class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    date_hired = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    objects=UserManager()

class Item(models.Model):
    item_name = models.CharField(max_length = 255)
    added_by = models.ForeignKey(User, related_name="my_items")
    created_at = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now = True)
    all_items = models.ManyToManyField(User, related_name="wishlists")
    objects=ItemManager()

