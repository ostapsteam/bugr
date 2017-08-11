import logging

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Bot
from .shortcuts import get_json
from .update import Update

log = logging.getLogger(__file__)


@csrf_exempt
def dispatch(request, botname):
    log.info("%s - call", botname)
    bot = get_object_or_404(Bot, name=botname)
    json_data = get_json(request.body.decode('utf-8'))
    resp = bot.handle(Update(json_data))
    return HttpResponse(resp)