from protos.models.proto import GeoProto
# from django.db import models


class Lab(GeoProto):

    def __unicode__(self):
        return "Lab #{}".format(self.id)
