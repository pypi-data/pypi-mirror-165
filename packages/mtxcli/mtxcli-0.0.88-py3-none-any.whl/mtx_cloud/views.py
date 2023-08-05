import os
import json
import time
import math
from requests import request
import boto3
import django
# from authlib.integrations.django_client import OAuth
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.http import HttpResponse, FileResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from urllib.parse import quote_plus, urlencode
from django import forms
# from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView, FormView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from rest_framework import serializers, viewsets, routers
from django.forms.models import model_to_dict
from functools import wraps
from .models import SshHost
import logging
logger = logging.getLogger(__name__)
User = get_user_model()



class SshHostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SshHost
        # fields = ['title','host']
        fields = '__all__'

# ViewSets define the view behavior.
class SshHostViewSet(viewsets.ModelViewSet):
    queryset = SshHost.objects.all()
    serializer_class = SshHostSerializer
    

def image_list(request):
    """列出图片和相关的变体"""
    pass

def meta(r):
    chat_api = settings.MTX_CHAT_API
    return JsonResponse({
        'chat_api': chat_api,
        'graphql_api': '/graphql/',
    })

def chat_demo(r):
    """试试触发websocket 消息发送"""

    websocket_event_bust_name = "WSChatEventBus"
    message_object = {
                    'message': 'django_message1',
                    'chatId': 'DEFAULT',
                    'senderConnectionId': 'senderConnectionId123',
                }
    client = boto3.client('events')
    
    #发送消息
    response = client.put_events(
        Entries=[
            {
                'EventBusName': websocket_event_bust_name,
                'Source': 'ChatApplication',
                'DetailType': 'ChatMessageReceived',
                'Detail': json.dumps(message_object),
            },
        ],
        # EndpointId='string'
    )
    return JsonResponse({
        'response': response,
    })
 
def install(r):
     """通过url触发安装命令"""
     from django.core.management import call_command
     call_command("mtx_collectstatic")
     return JsonResponse({"result":'install finished'})