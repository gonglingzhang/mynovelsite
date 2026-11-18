from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponse
from . import views

app_name = "novel_others"
urlpatterns = [
    path('about_us/',views.novel_about_us,name='reverse_novel_about_us'),
    path('contact_us/',views.novel_contact_us,name='reverse_novel_contact_us'),
    path('suggest_us/',views.novel_suggest_us,name='reverse_novel_suggest_us'),
    path('friend_links/',views.novel_friend_links,name='reverse_novel_friend_links'),
     path('my_suggestions/', views.novel_my_suggestions, name='reverse_novel_my_suggestions'),
     path('my_suggestions/delete/<int:suggest_id>/', views.delete_suggest, name='reverse_delete_suggest'),
]
