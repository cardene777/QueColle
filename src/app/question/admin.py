from django.contrib import admin
from .models import QuestionCollection, Question, Data, QuestionTime


class QuestionCollectionAdmin(admin.ModelAdmin):
    list_display = ('collection', 'user', 'about', 'attention', 'numbers')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('collection', 'question', 'correct', 'explanation')


class DataAdmin(admin.ModelAdmin):
    list_display = ('collection', 'question', 'number', 'user', 'judge', 'answer_time',
                    'correct_answer', 'user_answer')


class QuestionTimeAdmin(admin.ModelAdmin):
    list_display = ('collection', 'number', 'time')


admin.site.register(QuestionCollection, QuestionCollectionAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Data, DataAdmin)
admin.site.register(QuestionTime, QuestionTimeAdmin)
