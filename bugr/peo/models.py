from django.db import models
from protos.models.proto import Proto

class Lab(models.Model):

    def __unicode__(self):
        return "Lab #{}".format(self.id)
