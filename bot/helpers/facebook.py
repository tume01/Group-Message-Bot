from typing import Dict, List, Any
from django.conf import settings
import requests


class FacebookHelper(object):

    @staticmethod
    def send_message(recipient_id: str, message: str) -> bool:
        params = {
            'access_token': settings.BOT_APP_TOKEN
        }

        data = {
            'recipient': {
                'id': recipient_id
            },
            'message': {'text': message},
        }

        r = requests.post(settings.FACEBOOK_GRAPH_URL + '/me/messages', params=params, json=data)
        return r.status_code == 200

    @staticmethod
    def post_group(group_id: str, message: str, media: str = None) -> bool:
        data = {
            'access_token': settings.BOT_APP_TOKEN,
            'message': message,
            'link': media,
        }

        post_url = '{url}/{group_id}/feed'.format(url= settings.FACEBOOK_GRAPH_URL, group_id=group_id)
        r = requests.post(post_url, params=data)
        return r.status_code == 200

    @staticmethod
    def post_back_button(title, payload) -> Dict[str,str]:
        return {
            'type': 'postback',
            'title': title,
            'payload': payload
        }

    @staticmethod
    def send_buttons(recipient_id: str, message: str, buttons: List[Dict[str,str]]) -> bool:
        params = {
            'access_token': settings.BOT_APP_TOKEN
        }

        data = {
            'recipient': {
                'id': recipient_id
            },
            'message': {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'button',
                        'text': message,
                        'buttons': buttons,
                    }
                }
            }
        }
        r = requests.post(settings.FACEBOOK_GRAPH_URL + '/me/messages', params=params, json=data)
        return r.status_code == 200

    @staticmethod
    def send_carousel(recipient_id: str, generic_templates: Any) -> bool:
        params = {
            'access_token': settings.BOT_APP_TOKEN
        }

        data = {
            'recipient': {
                'id': recipient_id
            },
            'message': {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'generic',
                        'elements': generic_templates,
                    }
                }
            }
        }
        r = requests.post(settings.FACEBOOK_GRAPH_URL + '/me/messages', params=params, json=data)
        return r.status_code == 200

    @staticmethod
    def get_user(user_id: str, properties: List[str]) -> Dict[str,str]:
        params = {
            'access_token': settings.BOT_APP_TOKEN,
        }

        r = requests.get(settings.FACEBOOK_GRAPH_URL + '/{id}'.format(id=user_id), params=params)
        return r.json()

    @staticmethod
    def get_groups(user_id: str) -> Dict[str,str]:
        params = {
            'access_token': settings.BOT_APP_TOKEN,
        }

        r = requests.get(settings.FACEBOOK_GRAPH_URL + '/{id}/groups'.format(id=user_id), params=params)
        return r.json()
