from django.db import models
from django.urls import reverse


class QuestionCollection(models.Model):
    class Meta:
        verbose_name = '問題集タイトル'
        verbose_name_plural = '問題集タイトル'

    collection = models.CharField(
        verbose_name='問題集名',
        max_length=250
    )

    user = models.CharField(
        verbose_name="問題集作成ユーザー",
        max_length=100,
        default="Who"
    )

    about = models.TextField(
        verbose_name='問題集概要'
    )

    image = models.ImageField(
        verbose_name='画像',
        upload_to='images/',
        default='default_image/question.png',
        blank=True,
    )

    attention = models.TextField(
        verbose_name="注意事項",
        blank=True
    )

    numbers = models.IntegerField(
        verbose_name="問題グループ数",
        default=1,
        blank=True
    )

    def __str__(self):
        return str(self.collection)

    def get_absolute_url(self):
        return reverse('question:about', kwargs={'pk': self.pk})


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
        verbose_name='解説',
        blank=True
    )

    def __str__(self):
        return str(self.question)

    def get_absolute_url(self):
        return reverse('question:about', kwargs={'pk': self.pk})


class Data(models.Model):
    class Meta:
        verbose_name = '解答データ'
        verbose_name_plural = '解答データ'

    collection = models.ForeignKey(
        QuestionCollection,
        verbose_name='所属問題集名',
        on_delete=models.CASCADE
    )

    question = models.ForeignKey(
        Question,
        verbose_name='所属問題',
        on_delete=models.CASCADE
    )

    number = models.IntegerField(
        verbose_name="グループ番号"
    )

    user = models.CharField(
        verbose_name="ユーザー名",
        max_length=100
    )

    CHOICES_JUDGE = (
        ("正解", "good"),
        ("不正解", "bad"),
    )

    judge = models.CharField(
        verbose_name="正誤",
        max_length=10,
        choices=CHOICES_JUDGE
    )

    answer_time = models.IntegerField(
        verbose_name="解答時間",
        default=10000
    )

    correct_answer = models.TextField(
        verbose_name="問題正解",
    )

    user_answer = models.TextField(
        verbose_name="ユーザー解答"
    )

    def __str__(self):
        return str(self.user)


class QuestionTime(models.Model):
    class Meta:
        verbose_name = '問題群設定'
        verbose_name_plural = '問題群設定'

    collection = models.ForeignKey(
        QuestionCollection,
        verbose_name="問題集",
        on_delete=models.CASCADE
    )

    number = models.IntegerField(
        verbose_name="問題群"
    )

    time = models.DateTimeField(
        verbose_name="解答時間設定"
    )

    def __str__(self):
        return str(self.time)
