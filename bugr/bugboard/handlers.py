import logging
import re

log = logging.getLogger(__file__)
CMD = {}
DESC = {}


def register(l, desc=None):
    def decorator(f):
        label = re.compile(l)
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


def call(bot, update, cmd, *args):
    fn, fargs = find_command(cmd)
    log.info("Call %s%r", cmd, tuple(args))
    try:
        return fn(bot, update, *args, **fargs)
    except:
        log.exception("Error")


def find_command(cmd):
    for pattern, fn in CMD.items():
        result = re.match(pattern, cmd)
        if result:
            return fn, result.groupdict()
    return None, None
