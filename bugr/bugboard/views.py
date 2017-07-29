from django.http import HttpResponse, Http404
from .models import Bot
import logging

log = logging.getLogger(__file__)


def dispatch(request, botname):
    log.info("%s - call", botname)
    try:
        bot = Bot.get(name=botname)
    except Bot.DoesNotExist:
        raise Http404("Bot {} doesn't exist".format(botname))
    return HttpResponse("1")