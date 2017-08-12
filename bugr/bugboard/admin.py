from django.contrib import admin
from .models import Bot, TUser, Proposal, Question, Dialog

admin.site.register(Bot)
admin.site.register(TUser)
admin.site.register(Proposal)
admin.site.register(Question)
admin.site.register(Dialog)
