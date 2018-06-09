# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Message, Conversation


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'text',
    )

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'sender_id',
        'recipient_id',
        'status',
    )

