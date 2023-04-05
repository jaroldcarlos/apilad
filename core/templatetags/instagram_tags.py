from django import template
from django.shortcuts import render
from instagram.client import InstagramAPI

register = template.Library()

@register.inclusion_tag('templatetags/instagram.html')
def show_instagram_posts():
    access_token = "IGQVJYSjFhT0kyUFBqQnZAvZAnUxS1NaU2d4U2JZAWW1FbWZAiTlE5NEgxZAVRVRFZAtMUFsa1VCWjl2UkFaVDB6ay1tR0hUR3ZA0TDNaNGo0ZAzhZAeVZAoZAVY0T2VFampiR2h1T1FkQ0VnWHRzZADM2cHFrMjdXTQZDZD"
    api = InstagramAPI(access_token=access_token)
    recent_media, next_ = api.user_recent_media(user_id="53617619637", count=10)
    context = {
        'posts': recent_media,
    }
    return context
