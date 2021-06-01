from django import forms
from .models import QuestionCollection, Question


class QuestionCollectionForm(forms.ModelForm):
    class Meta:
        model = QuestionCollection
        fields = ('collection', 'user', 'about', 'image', 'attention')

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
