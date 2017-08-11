from bugr.bugboard.bots.register import register, render_cmd, ParseMode
from bugr.bugboard.models import TUser, Proposal
import logging

log = logging.getLogger(__file__)


@register("^/create_request$", desc="создать заявку")
def create_requests(bot, update):
    text = "Создать заявку\n\n"
    bot.sendMessage(chat_id=update.chat_id, text=text)


@register("^/help$", desc="помощь")
def help(bot, update):
    text = "Хелпер\n\n" + "\n".join([render_cmd(x) for x in ("/my_requests", "/create_request")])
    bot.sendMessage(chat_id=update.chat_id, text=text)


@register("^/my_requests$", desc="мои заявки")
def my_requests(bot, update):
    sender = TUser.get_user(**update.sender)
    proposals = Proposal.objects.filter(
        asignee=sender,
        deleted_at__isnull=True
    )
    count = proposals.count()
    if count:
        text = "Мои заявки ({})\n\n".format(count)
        proposals = proposals.order_by("-id")[:5]
        text += "\n".join([str(p) for p in proposals])
    else:
        text = "У Вас нет актиных заявок\n\n" + "\n".join([render_cmd(x) for x in ("/create_request", "/help")])
    bot.sendMessage(chat_id=update.chat_id, text=text)


@register("^/req(?P<proposal_id>[0-9]+)$")
def req(bot, update, proposal_id):
    sender = TUser.get_user(**update.sender)
    try:
        proposal = Proposal.objects.get(id=proposal_id, asignee=sender)
        text = "*{}*\n".format(proposal.name)
        if proposal.created_by:
            text += "{} _{:%m.%d.%Y %H:%m}_\n".format(proposal.created_by, proposal.created_at)
        text += str(proposal.desc)
        bot.sendMessage(chat_id=update.chat_id, text=text, parse_mode=ParseMode.Markdown.value)
    except Proposal.DoesNotExist:
        log.warn("'%s' doesn't exist but queried", proposal)
