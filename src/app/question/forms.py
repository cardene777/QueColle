from django import forms
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput

from .models import QuestionCollection, Question, QuestionSchedule


class QuestionCollectionForm(forms.ModelForm):
    class Meta:
        model = QuestionCollection
        fields = ('collection', 'user', 'about', 'image', 'attention', 'numbers')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['collection'].widget.attrs['class'] = 'form-control'
        self.fields['collection'].widget.attrs['id'] = 'collection'
        self.fields['collection'].widget.attrs['name'] = 'collection'
        self.fields['collection'].widget.attrs['placeholder'] = '問題集名'

        self.fields['user'].widget.attrs['class'] = 'form-control'
        self.fields['user'].widget.attrs['id'] = 'user'
        self.fields['user'].widget.attrs['name'] = 'user'
        self.fields['user'].widget.attrs['placeholder'] = 'ユーザー名'

        self.fields['about'].widget.attrs['class'] = 'form-control'
        self.fields['about'].widget.attrs['id'] = 'about'
        self.fields['about'].widget.attrs['name'] = 'about'
        self.fields['about'].widget.attrs['placeholder'] = '概要'

        self.fields['image'].widget.attrs['class'] = 'image'
        self.fields['image'].widget.attrs['placeholder'] = '画像(任意)'

        self.fields['attention'].widget.attrs['class'] = 'form-control'
        self.fields['attention'].widget.attrs['id'] = 'attention'
        self.fields['attention'].widget.attrs['name'] = 'attention'
        self.fields['attention'].widget.attrs['placeholder'] = '注意事項'

        self.fields['numbers'].widget.attrs['class'] = 'form-control'
        self.fields['numbers'].widget.attrs['id'] = 'numbers'
        self.fields['numbers'].widget.attrs['name'] = 'numbers'
        self.fields['numbers'].widget.attrs['placeholder'] = '問題グループ数'


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('collection', 'question', 'correct', 'explanation')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['collection'].widget.attrs['class'] = 'form-control'
        self.fields['collection'].widget.attrs['id'] = 'collection'
        self.fields['collection'].widget.attrs['name'] = 'collection'
        self.fields['collection'].widget.attrs['placeholder'] = '問題集名'

        self.fields['question'].widget.attrs['class'] = 'form-control'
        self.fields['question'].widget.attrs['id'] = 'question'
        self.fields['question'].widget.attrs['name'] = 'question'
        self.fields['question'].widget.attrs['placeholder'] = '問題文'

        self.fields['correct'].widget.attrs['class'] = 'form-control'
        self.fields['correct'].widget.attrs['id'] = 'correct'
        self.fields['correct'].widget.attrs['name'] = 'correct'
        self.fields['correct'].widget.attrs['placeholder'] = '正解'

        self.fields['explanation'].widget.attrs['class'] = 'form-control'
        self.fields['explanation'].widget.attrs['id'] = 'explanation'
        self.fields['explanation'].widget.attrs['name'] = 'explanation'
        self.fields['explanation'].widget.attrs['placeholder'] = '解説'


class QuestionScheduleForm(forms.ModelForm):
    class Meta:
        model = QuestionSchedule
        fields = ('collection', 'number', 'start_date', 'start_time', 'end_date', 'end_time')
        widgets = {
            'start_date': DatePickerInput(
                format='%Y-%m-%d',
                options={
                    'locale': 'ja',
                    'dayViewHeaderFormat': 'YYYY年 MMMM',
                }
            ).start_of("期間"),
            'start_time': TimePickerInput(
                format='%H:%M:%S',
                options={
                    'locale': 'ja',
                }
            ),
            'end_date': DatePickerInput(
                format='%Y-%m-%d',
                options={
                    'locale': 'ja',
                    'dayViewHeaderFormat': 'YYYY年 MMMM',
                }
            ).end_of("期間"),
            'end_time': TimePickerInput(
                format='%H:%M:%S',
                options={
                    'locale': 'ja',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['collection'].widget.attrs['class'] = 'form-control'
        self.fields['collection'].widget.attrs['id'] = 'collection'
        self.fields['collection'].widget.attrs['name'] = 'collection'
        self.fields['collection'].widget.attrs['placeholder'] = '問題集名'

        self.fields['number'].widget.attrs['class'] = 'form-control'
        self.fields['number'].widget.attrs['id'] = 'number'
        self.fields['number'].widget.attrs['name'] = 'number'
        self.fields['number'].widget.attrs['placeholder'] = '問題集番号'

