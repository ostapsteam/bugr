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
           "/мои_заявки\n" \
           "/подать_заявку\n\n"


def call(cmd, *args):
    if cmd not in CMD:
        return
    log.info("Call %s%r", cmd, tuple(args))
    try:
        return CMD[cmd](*args)
    except:
        log.exception("Error")