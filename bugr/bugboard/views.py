import json
import logging

from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from .models import Bot

log = logging.getLogger(__file__)


@csrf_exempt
def dispatch(request, botname):
    log.info("%s - call", botname)
    try:
        bot = Bot.objects.get(name=botname)
    except Bot.DoesNotExist:
        raise Http404("Bot {} doesn't exist".format(botname))
    json_data = json.loads(request.body.decode('utf-8'))
    resp = bot.handle(json_data)
    return HttpResponse(resp)