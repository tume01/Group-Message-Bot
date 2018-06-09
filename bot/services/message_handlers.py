from typing import Any, List, Optional
import bot.utils.messages as messages
from bot.utils.patterns import Handler, Singleton
from bot.helpers.facebook import FacebookHelper
from bot.helpers.templates import Templates
from django.template import loader
from bot.models import EventMessage, FacebookTextMessage, FacebookTextMessageType, Message, Conversation, SelectedGroup
import datetime


class FacebookGetStartedHandler(Handler):

    def is_valid(self, request: Any) -> bool:
        return isinstance(request, FacebookTextMessage) \
            and request.type is FacebookTextMessageType.QUICK_REPLY \
            and request.text == 'START'

    def perform(self, request: Any) -> None:
        conversation, created = Conversation.objects.get_or_create(
            sender_id=request.recipient_id,
            recipient_id=request.sender_id,
        )
        FacebookHelper.send_message(request.sender_id, messages.GREETINGS_MESSAGE)
        buttons = Templates.options_buttons()
        if FacebookHelper.send_buttons(request.sender_id, messages.OPTIONS_MESSAGE, buttons):
            Message.objects.create(
                text=request.text,
                recipient_id=request.sender_id,
                sender_id=request.recipient_id
            )

class FacebookSelectGroupsHandler(Handler):

    def is_valid(self, request: Any) -> bool:
        return  isinstance(request, FacebookTextMessage) \
            and request.type is FacebookTextMessageType.QUICK_REPLY \
            and request.text == messages.CHECK_GROUPS_PAYLOAD

    def perform(self, request: Any) -> None:
        conversation, created = Conversation.objects.get_or_create(
            sender_id=request.recipient_id,
            recipient_id=request.sender_id,
        )
        groups = FacebookHelper.get_groups(request.sender_id).get('data')
        conversation.status = Conversation.SELECT_GROUPS_STATUS
        conversation.save()
        if FacebookHelper.send_carousel(request.sender_id, Templates.groups_carousel(groups)):
            Message.objects.create(
                text=request.text,
                recipient_id=request.sender_id,
                sender_id=request.recipient_id
            )

class SelectedGroupHandler(Handler):

    def is_valid(self, request: Any) -> bool:
        return  isinstance(request, FacebookTextMessage) \
            and request.type is FacebookTextMessageType.QUICK_REPLY \
            and messages.ADD_GROUP_PAYLOAD in request.text

    def perform(self, request: Any) -> None:
        conversation, created = Conversation.objects.get_or_create(
            sender_id=request.recipient_id,
            recipient_id=request.sender_id,
        )

        _, _, group_id = request.text.split('_')

        selected_group, created = SelectedGroup.objects.get_or_create(
            conversation_id=conversation.pk,
            status=SelectedGroup.SELECTED_STATUS,
            group_id=group_id
        )

        buttons = Templates.options_buttons()
        if FacebookHelper.send_buttons(request.sender_id, messages.OPTIONS_MESSAGE, buttons):
            Message.objects.create(
                text=request.text,
                recipient_id=request.sender_id,
                sender_id=request.recipient_id
            )

class BroadcastHandler(Handler):

    def is_valid(self, request: Any) -> bool:
        return  isinstance(request, FacebookTextMessage) \
            and request.type is FacebookTextMessageType.QUICK_REPLY \
            and request.text == messages.NEW_POST_PAYLOAD

    def perform(self, request: Any) -> None:
        conversation, created = Conversation.objects.get_or_create(
            sender_id=request.recipient_id,
            recipient_id=request.sender_id,
        )

        selected_groups = conversation.selected_groups.filter(status=SelectedGroup.SELECTED_STATUS)
        if len(selected_groups) > 0:
            conversation.status = Conversation.MESSAGE_STATUS
            conversation.save()
            if FacebookHelper.send_message(request.sender_id, messages.REQUEST_MESSAGE):
                Message.objects.create(
                    text=request.text,
                    recipient_id=request.sender_id,
                    sender_id=request.recipient_id
                )

        else:
            groups = FacebookHelper.get_groups(request.sender_id).get('data')
            conversation.status = Conversation.SELECT_GROUPS_STATUS
            conversation.save()
            FacebookHelper.send_message(request.sender_id, messages.SELECTED_GROUP_MESSAGE)
            if FacebookHelper.send_carousel(request.sender_id, Templates.groups_carousel(groups)):
                Message.objects.create(
                    text=request.text,
                    recipient_id=request.sender_id,
                    sender_id=request.recipient_id
                )

class RequestMessageHandler(Handler):

    def is_valid(self, request: Any) -> bool:
        conversation, created = Conversation.objects.get_or_create(
            sender_id=request.recipient_id,
            recipient_id=request.sender_id,
        )
        return  isinstance(request, FacebookTextMessage) \
            and request.type is FacebookTextMessageType.PLAIN_TEXT \
            and conversation.status == Conversation.MESSAGE_STATUS

    def perform(self, request: Any) -> None:
        conversation, created = Conversation.objects.get_or_create(
            sender_id=request.recipient_id,
            recipient_id=request.sender_id,
        )
        selected_groups = conversation.selected_groups.filter(status=SelectedGroup.SELECTED_STATUS)
        for selected_group in selected_groups:
            FacebookHelper.post_group(selected_group.group_id, request.text)
            selected_group.status = SelectedGroup.CLOSED_STATUS
            selected_group.save()
        conversation.status = Conversation.MESSAGE_STATUS
        conversation.save()
        FacebookHelper.send_message(request.sender_id, messages.CONFIRM_MESSAGE)
        buttons = Templates.options_buttons()
        if FacebookHelper.send_buttons(request.sender_id, messages.OPTIONS_MESSAGE, buttons):
            Message.objects.create(
                text=request.text,
                recipient_id=request.sender_id,
                sender_id=request.recipient_id
            )

class FacebookTextHandler(Handler):

    def is_valid(self, request: Any) -> bool:
        return isinstance(request, FacebookTextMessage) and request.type is FacebookTextMessageType.PLAIN_TEXT

    def perform(self, request: Any) -> None:
        if FacebookHelper.send_message(request.sender_id, request.text):
            Message.objects.create(
                text=request.text,
                recipient_id=request.sender_id,
                sender_id=request.recipient_id
            )

class FacebookMediaHandler(Handler):

    def is_valid(self, request: Any) -> bool:
        return False

    def perform(self, request: Any) -> None:
        pass

class MessageHandlerManager(metaclass=Singleton):

    def __init__(self):
        default_handler = FacebookTextHandler()
        request_message_handler = RequestMessageHandler(default_handler)
        broadcast_message_handler = BroadcastHandler(request_message_handler)
        selected_group_handler = SelectedGroupHandler(broadcast_message_handler)
        select_group_handler = FacebookSelectGroupsHandler(selected_group_handler)
        media_handler = FacebookMediaHandler(select_group_handler)
        self.base_handler = FacebookGetStartedHandler(media_handler)

