from .facebook import FacebookHelper
import bot.utils.messages as messages
from typing import Dict, List, Any

class Templates:
    """docstring for Templates"""

    @staticmethod
    def options_buttons() -> List[Dict[str,str]]:
        return [
            FacebookHelper.post_back_button(messages.NEW_POST_TITLE, messages.NEW_POST_PAYLOAD),
            FacebookHelper.post_back_button(messages.CHECK_GROUPS_TITTLE, messages.CHECK_GROUPS_PAYLOAD),
        ]

    @staticmethod
    def generic_element(title: str, buttons: Dict[str,str]=None) -> Dict[str,str]:
        element = {
            'title': title,
        }

        if buttons:
            element['buttons'] = buttons

        return element

    @staticmethod
    def add_group_buttons(group: Dict[str,str]) -> Dict[str,str]:
        return [
            FacebookHelper.post_back_button(messages.ADD_GROUP_TITTLE, messages.ADD_GROUP_PAYLOAD + group.get('id')),
        ]


    @staticmethod
    def groups_carousel(groups: Dict[str,str]) -> List[Dict[str,str]]:
        carousel = []
        for group in groups:
            buttons = Templates.add_group_buttons(group)
            carousel.append(Templates.generic_element(group.get('name'), buttons))
        return carousel
