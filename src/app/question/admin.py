from django.contrib import admin
from .models import QuestionCollection, Question

admin.site.register(QuestionCollection)
admin.site.register(Question)