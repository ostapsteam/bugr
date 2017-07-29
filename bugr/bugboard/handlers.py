import logging

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
    desc_text = desc if desc else DESC.get(label)
    text = label
    if desc_text:
        text += " - " + desc_text
    return text


def call(update, cmd, *args):
    if cmd not in CMD:
        return
    log.info("Call %s%r", cmd, tuple(args))
    try:
        return CMD[cmd](update, *args)
    except:
        log.exception("Error")