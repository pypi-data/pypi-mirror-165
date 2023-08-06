from django.contrib import admin
from .models import Action, States, TransitionManager , Flowmodel , SignList
# Register your models here.
from django.conf import settings




admin.site.register(Flowmodel)
admin.site.register(TransitionManager)
admin.site.register(Action )
admin.site.register(States)
admin.site.register(SignList) 
