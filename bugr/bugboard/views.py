from django.http import HttpResponse
import logging

log = logging.getLogger(__file__)

# Create your views here.
def dispatch(request, bot):
    log.info("%s - call", bot)
    return HttpResponse("1")