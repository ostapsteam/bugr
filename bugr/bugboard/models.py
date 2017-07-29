from django.db import models
from datetime import datetime


class TUser(models.Model):
    uid = models.CharField(max_length=16, null=False, blank=False, unique=True)
    name = models.CharField(max_length=128, blank=False, null=False)

    joined_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __repr__(self):
        return "#{} ({})".format(self.uid, self.name)


class Proto(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    desc = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(TUser, null=False, blank=False, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)

    updated_by = models.ForeignKey(TUser, null=False, blank=False, related_name='+')
    updated_at = models.DateTimeField(auto_now=True, blank=False, null=False)

    deleted_by = models.ForeignKey(TUser, null=True, blank=True, related_name='+')
    deleted_at = models.DateTimeField(blank=True, null=True)

    @property
    def is_active(self):
        return self.deleted_by is None

    def delete(self, user):
        self.deleted_by = user
        self.deleted_at = datetime.utcnow()
        self.save()

    class Meta:
        abstract = True


class Bot(Proto):
    name = models.CharField(max_length=128, null=False, blank=False, unique=True)
    token = models.CharField(max_length=128, null=False, blank=False)

    def __repr__(self):
        return self.name