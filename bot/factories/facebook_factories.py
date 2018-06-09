from typing import Optional, Dict
from bot.utils.patterns import AbstractMessageFactory, Singleton
from bot.models import EventMessage, FacebookTextMessage, FacebookTextMessageType

class FacebookMessageFactory(AbstractMessageFactory):

    def build_text_message(self, json_object: Dict[str,str]) -> EventMessage:
        try:
            sender_id = json_object.get('sender').get('id')
            recipient_id = json_object.get('recipient').get('id')
            timestamp = json_object.get('timestamp')
            text = json_object.get('message').get('text')
            message_type = FacebookTextMessageType.PLAIN_TEXT
            return FacebookTextMessage(sender_id, recipient_id, timestamp, text, message_type)
        except Exception as e:
            raise e

    def build_media_message(self, json_object: Dict[str,str]) -> EventMessage:
        pass

    def build_postback_message(self, json_object: Dict[str,str]) -> EventMessage:
        try:
            sender_id = json_object.get('sender').get('id')
            recipient_id = json_object.get('recipient').get('id')
            timestamp = json_object.get('timestamp')
            payload = json_object.get('postback').get('payload')
            message_type = FacebookTextMessageType.QUICK_REPLY
            return FacebookTextMessage(sender_id, recipient_id, timestamp, payload, message_type)
        except Exception as e:
            raise e

class MessageFactory(metaclass=Singleton):

    def make(self, json_object: Dict[str,str]) -> Optional[EventMessage]:
        message = json_object.get('message')
        if message and 'text' in message:
            return FacebookMessageFactory().build_text_message(json_object)
        postback = json_object.get('postback')
        if postback:
            return FacebookMessageFactory().build_postback_message(json_object)
        return None
