from django.contrib import admin
from .models import QuestionCollection, Question, Data


class QuestionCollectionAdmin(admin.ModelAdmin):
    list_display = ('collection', 'user', 'about', 'attention')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('collection', 'question', 'correct', 'explanation')


class DataAdmin(admin.ModelAdmin):
    list_display = ('collection', 'question', 'user', 'judge', 'answer_time',
                    'correct_answer', 'user_answer')


admin.site.register(QuestionCollection, QuestionCollectionAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Data, DataAdmin)
