from django.http import HttpResponse, Http404
from .models import Bot
import logging
import json

log = logging.getLogger(__file__)


def dispatch(request, botname):
    log.info("%s - call", botname)
    try:
        bot = Bot.objects.get(name=botname)
    except Bot.DoesNotExist:
        raise Http404("Bot {} doesn't exist".format(botname))
    json_data = json.loads(request.body)
    resp = bot.handle(json_data)
    return HttpResponse(resp)