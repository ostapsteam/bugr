from django.db import models
from datetime import datetime
import logging
import requests

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

    def handle(self, request):
        log.info("Req: %s", requests)
        chat_id = request["chat"]["id"]
        text = request["message"]["text"]
        self.sendMessage(chat_id=chat_id, text="Recieve: " + text)


