import logging

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .bots.register import register, ParseMode
from .models import Bot, TUser, Proposal
from .shortcuts import get_json, reply_with_tpl
from .update import Update

log = logging.getLogger(__file__)


@csrf_exempt
def dispatch(request, botname):
    log.info("%s - call", botname)
    bot = get_object_or_404(Bot, name=botname)
    json_data = get_json(request.body.decode('utf-8'))
    resp = bot.handle(Update(json_data))
    return HttpResponse(resp)


# Handlers
@register("^/create_request$", desc="создать заявку")
@reply_with_tpl("myvortex/create_request.html")
def create_requests(bot, update):
    pass


@register("^/help$", desc="помощь")
@reply_with_tpl("myvortex/help.html")
def help(bot, update):
    pass


@register("^/my_requests$", desc="мои заявки")
@reply_with_tpl("myvortex/my_requests.html", parse_mode=ParseMode.Markdown.value)
def my_requests(bot, update):
    sender = TUser.get_user(**update.sender)
    proposals = Proposal.objects.filter(
        asignee=sender,
        deleted_at__isnull=True
    )
    count = proposals.count()
    proposals = proposals.order_by("-id")[:5]
    return {
        "proposals": proposals,
        "proposals_count": count
    }


@register("^/req(?P<proposal_id>[0-9]+)$")
@reply_with_tpl("myvortex/req.html", parse_mode=ParseMode.Markdown.value)
def req(bot, update, proposal_id):
    sender = TUser.get_user(**update.sender)
    try:
        proposal = Proposal.objects.get(id=proposal_id, asignee=sender)
        return {
            "proposal": proposal
        }
    except Proposal.DoesNotExist:
        log.warn("'%s' doesn't exist but queried", proposal)
