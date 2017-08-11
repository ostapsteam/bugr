import enum
import logging
from datetime import datetime

import requests
from django.db import models

from bugr.bugboard.bots.register import call, render_cmd, register
from .update import Update

log = logging.getLogger(__file__)


class Question(models.Model):
    dialog = models.ForeignKey('Dialog', null=False, blank=False)
    question_text = models.CharField(max_length=256, null=False, blank=False)
    answer_text = models.CharField(max_length=256, null=True, blank=True)

    is_sent = models.BooleanField(blank=False, null=False, default=False)
    skiped = models.BooleanField(blank=False, null=False, default=False)
    answered = models.BooleanField(blank=False, null=False, default=False)

    def skip(self):
        self.skiped = True
        self.answered = True

    def answer(self, text):
        self.answer_text = text
        self.answered = True

    def set_sent(self):
        self.is_sent = True


class Dialog(models.Model):
    closed = models.BooleanField(null=False, blank=False, default=False)
    terminated = models.BooleanField(null=False, blank=False, default=False)

    def get_question(self):
        return Question.objects.filter(answered=False).first()

    def add_question(self, question_text):
        Question.objects.create(dialog=self, question_text=question_text)


class TUser(models.Model):
    uid = models.CharField(max_length=16, null=False, blank=False, unique=True)
    first_name = models.CharField(max_length=128, blank=True, null=True)
    last_name = models.CharField(max_length=128, blank=True, null=True)
    language_code = models.CharField(max_length=16, blank=True, null=True)

    joined_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    dialog = models.ForeignKey(Dialog, null=True, blank=False)

    @property
    def name(self):
        return " ".join([x for x in (self.first_name, self.last_name) if x])

    @staticmethod
    def get_user(id, first_name, last_name, language_code):
        obj, created = TUser.objects.update_or_create(
            uid=id, defaults={
                "first_name": first_name,
                "last_name": last_name,
                "language_code": language_code
            }
        )
        if created:
            log.info("%s was created now", obj)
        else:
            log.info("%s was fetched", obj)
        return obj

    def start_dialog(self, questions):
        dialog = Dialog()
        for question in questions:
            dialog.add_question(question)

    def __str__(self):
        return "/user{} ({})".format(self.uid, self.name)


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

    asignee = models.ForeignKey(TUser, null=False, blank=False)

    def __str__(self):
        return "/req{} {}".format(self.id, self.name)


class Bot(Proto):
    name = models.CharField(max_length=128, null=False, blank=False, unique=True)
    token = models.CharField(max_length=128, null=False, blank=False)

    def __str__(self):
        return self.name

    def get_url(self, method):
        return "https://api.telegram.org/bot{}/{}".format(self.token, method)

    def sendMessage(self, **kwargs):
        log.info("Sending %s", kwargs)
        resp = requests.post(self.get_url("sendMessage"), data=kwargs)
        assert resp.ok, resp.reason

    def handle(self, update: Update):
        log.info("Req: %s", update)
        parts = update.prepare_command()
        if parts:
            cmd, *args = parts
            call(self, update, cmd, *args)
