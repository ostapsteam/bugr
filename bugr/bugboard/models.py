from django.db import models

# Create your models here.
class Profile(models.Model):
    uid = models.CharField(max_length=16, null=False, blank=False)
    name = models.CharField(max_length=128, null=False, blank=False)

    def __repr__(self):
        return "#{} ({})".format(self.uid, self.name)