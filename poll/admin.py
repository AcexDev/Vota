from django.contrib import admin
from .models import Poll, Options, Answer, Question

# Register your models here.
admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Options)
