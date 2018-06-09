# -*- coding: utf-8 -*-
from bot.models import Message, Conversation
from bot.serializers import MessageSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route
from django.http import HttpResponse, HttpResponseBadRequest
from rest_framework import status
from django.conf import settings
import hashlib
from django.db.models import Count
from .factories.facebook_factories import MessageFactory
from .services.message_handlers import MessageHandlerManager
import json
import requests
import hmac

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @list_route(methods=['post', 'get'])
    def webhook(self, request):
        if request.method == 'POST':
            sha_key, signature = request.META.get('HTTP_X_HUB_SIGNATURE').split('=')
            digester = hmac.new(settings.BOT_SECRET.encode(), request.body, hashlib.sha1)
            calculated_signature = digester.hexdigest()
            if signature == calculated_signature:
                request_data = json.loads(request.body)
                for entry in request_data.get('entry'):
                    for message_event in entry.get('messaging', []):
                        message = MessageFactory().make(message_event)
                        if message:
                            MessageHandlerManager().base_handler.handle_request(message)
            return Response(status=status.HTTP_200_OK)
        hub_challange = request.GET.get('hub.challenge')
        hub_token = request.GET.get('hub.verify_token')
        if hub_challange and hub_token == settings.HUB_CHALLANGE:
            return HttpResponse(hub_challange, content_type='text/plain')
        return HttpResponseBadRequest()
