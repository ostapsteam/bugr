import logging

log = logging.getLogger(__file__)
CMD = {}


def register(label):
    def decorator(f):
        CMD[label] = f
        return f
    return decorator


@register("/help")
def help():
    return "Хелпер\n\n" \
           "/my_requests - мои заявки\n" \
           "/create_request - создать заявку\n\n"


@register("/my_requests")
def my_requests():
    text = "Мои заявки\n\n"
    return text


@register("/create_request")
def create_requests():
    text = "Создать заявку\n\n"
    return text


def call(cmd, *args):
    if cmd not in CMD:
        return
    log.info("Call %s%r", cmd, tuple(args))
    try:
        return CMD[cmd](*args)
    except:
        log.exception("Error")