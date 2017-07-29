from django.db import models
from datetime import datetime
import logging
import requests
from .handlers import call, render_cmd, register

log = logging.getLogger(__file__)


class TUser(models.Model):
    uid = models.CharField(max_length=16, null=False, blank=False, unique=True)
    name = models.CharField(max_length=128, blank=False, null=False)

    joined_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __unicode__(self):
        return "#{} ({})".format(self.uid, self.name)


class Proto(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    desc = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(TUser, null=True, blank=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    updated_by = models.ForeignKey(TUser, null=True, blank=True, related_name='+')
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    deleted_by = models.ForeignKey(TUser, null=True, blank=True, related_name='+')
    deleted_at = models.DateTimeField(blank=True, null=True)

    @property
    def is_active(self):
        return self.deleted_at is None

    def delete(self, user):
        self.deleted_by = user
        self.deleted_at = datetime.utcnow()
        self.save()

    class Meta:
        abstract = True


class Proposal(Proto):

    def __unicode__(self):
        return "/req_{} - {}".format(self.id, self.name)


class Bot(Proto):
    name = models.CharField(max_length=128, null=False, blank=False, unique=True)
    token = models.CharField(max_length=128, null=False, blank=False)

    def __unicode__(self):
        return self.name

    def get_url(self, method):
        return "https://api.telegram.org/bot{}/{}".format(self.token, method)

    def sendMessage(self, **kwargs):
        resp = requests.post(self.get_url("sendMessage"), data=kwargs)
        assert resp.ok, resp.reason

    def handle(self, msg):
        log.info("Req: %r", msg)
        chat_id = msg["message"]["chat"]["id"]
        text = msg["message"]["text"]

        parts = self.prepare_command(text)
        if parts:
            cmd, *args = parts
            text = call(msg, cmd, *args)
            if text:
                self.sendMessage(chat_id=chat_id, text=text)

    def prepare_command(self, text):
        parts = text.split()
        if parts:
            cmd = parts[0]
            if len(cmd) > 1 and cmd.startswith("/"):
                return parts


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
