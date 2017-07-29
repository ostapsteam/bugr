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
    return "Хелпер"


def call(cmd, *args):
    log.info("Call %s%r", cmd, tuple(args))
    return CMD[cmd](*args)