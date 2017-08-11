import json

from django.core.exceptions import SuspiciousOperation
from django.template.loader import render_to_string


def get_json(data):
    try:
        return json.loads(data)
    except:
        raise SuspiciousOperation("Can't parse message")


def reply_with_tpl(tpl, parse_mode=None):
    def decor(f):
        def wrap(bot, update):
            ctx = f(bot, update)
            bot.sendMessage(
                chat_id=update.chat_id,
                text=render_to_string(tpl, ctx or {}),
                parse_mode=parse_mode
            )
        return wrap
    return decor
