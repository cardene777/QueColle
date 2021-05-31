from django.db import models


class QuestionCollection(models.Model):
    class Meta:
        verbose_name = '問題集タイトル'
        verbose_name_plural = '問題集タイトル'

    collection = models.CharField(
        verbose_name='問題集名',
        max_length=250
    )

    about = models.TextField(
        verbose_name='問題集概要'
    )

    image = models.ImageField(
        verbose_name='画像',
        upload_to='images/',
        default='images/question.png',
        blank=True,
    )

    attention = models.TextField(
        verbose_name="注意事項",
        blank=True
    )

    def __str__(self):
        return str(self.collection)


class Question(models.Model):
    class Meta:
        verbose_name = '問題'
        verbose_name_plural = '問題'

    collection = models.ForeignKey(
        QuestionCollection,
        verbose_name='所属問題集名',
        on_delete=models.CASCADE
    )

    question = models.TextField(
        verbose_name='問題文'
    )

    correct = models.TextField(
        verbose_name='正解'
    )

    explanation = models.TextField(
        verbose_name='解説'
    )

    def __str__(self):
        return str(self.question)


