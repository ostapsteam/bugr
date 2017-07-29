import logging
from .models import Proposal

log = logging.getLogger(__file__)
CMD = {}
DESC = {}


def register(label, desc=None):
    def decorator(f):
        CMD[label] = f
        if desc:
            DESC[label] = desc
        return f
    return decorator


def render_cmd(label, desc=None):
    return "{} - {}".format(label, desc if desc else DESC[label])


@register("/help", desc="помощь")
def help(update):
    return "Хелпер\n\n" + "\n".join([render_cmd(x) for x in ("/my_requests", "create_request")])


@register("/my_requests", desc="мои заявки")
def my_requests(update):
    count = Proposal.objects.count()
    if count:
        text = "Мои заявки ({})\n\n".format(count)
        proposals = Proposal.objects.order_by("-id")[:5]
        text += "\n".join(proposals)
    else:
        text = "У Вас нет актиных заявок\n\n" + "\n".join([render_cmd(x) for x in ("create_request", "/help")])
    return text


@register("/create_request", desc="создать заявку")
def create_requests(update):
    text = "Создать заявку\n\n"
    return text


def call(update, cmd, *args):
    if cmd not in CMD:
        return
    log.info("Call %s%r", cmd, tuple(args))
    try:
        return CMD[cmd](update, *args)
    except:
        log.exception("Error")