from django.http import HttpResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

from .models import QuestionCollection, Question
from django.views import generic
from typing import List
import random
import time
import csv


class QuestionHome(generic.ListView):
    template_name: str = "question/question_home.html"
    model = QuestionCollection
    context_object_name: str = "question_collects"
    paginate_by: int = 10

    def get_queryset(self):
        question_collections = QuestionCollection.objects.all()
        if 'q' in self.request.GET and self.request.GET['q'] is not None:
            q = self.request.GET['q']
            question_collections = question_collections.filter(collection__icontains=q)
        # username = self.request.user.username
        return question_collections


class QuestionAbout(generic.DetailView):
    template_name: str = "question/question_about.html"
    model = QuestionCollection
    context_object_name: str = "question_collection"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection_name = QuestionCollection.objects.get(id=self.kwargs['pk'])
        context["length"] = Question.objects.filter(collection=collection_name).count()
        return context


def question(requests, collection_id: int) -> str:
    """
    random choice question
    :param requests: requests
    :param collection_id: int
    :return: html file with one questions
    """
    # 全て解答し終わった時の処理
    try:
        if requests.POST["questions"] == "[]":
            params: dict = {
                "message": "お疲れ様でした！"
            }
            return render(requests, 'question/answer_done.html', params)
    except MultiValueDictKeyError:
        pass
    message: str = "question"
    # ランダムに問題を取得
    collection_name: str = QuestionCollection.objects.get(id=collection_id)
    try:
        questions: List[int] = eval(requests.POST["questions"])
    except:
        questions: List[int] = list(Question.objects.filter(collection=collection_name).values_list("id", flat=True))
    one_question: int = random.choice(questions)
    questions.remove(one_question)
    one_questions: dict = Question.objects.get(id=one_question)
    # 問題番号取得
    question_counts: int = Question.objects.filter(collection=collection_name).count()
    question_number: int = question_counts - len(questions)
    start_time: time = time.time()
    params: dict = {
        "collection_id": collection_id,
        "questions": questions,
        "one_questions": one_questions,
        "question_number": question_number,
        "start_time": start_time,
    }
    return render(requests, 'question/question.html', params)


def answer(requests):
    if requests.method == "POST":
        # 解答時間計算
        start_time = float(requests.POST['start_time'].replace(",", '').replace('"', '').replace("'", ""))
        end_time = time.time()
        answer_time = end_time - start_time
        message: str = "answer"
        judge: str = "不正解"
        questions: str = requests.POST["questions"]
        question_id: int = requests.POST["question_id"]
        user_answer: str = requests.POST["answer"]
        correct_answer: str = Question.objects.get(id=question_id)
        if str(correct_answer) == str(user_answer):
            judge: str = "正解"

        params: dict = {
            "questions": questions,
            "message": message,
            "judge": judge,
            "correct_answer": correct_answer,
            "collection_id": requests.POST["collection_id"]
        }
        return render(requests, 'question/question.html', params)


# def data_export(request):
#     """
#     data export csv file
#     :param request:
#     :return: csv file
#     """
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="data.csv"'
#     # HttpResponseオブジェクトはファイルっぽいオブジェクトなので、csv.writerにそのまま渡せます。
#     writer = csv.writer(response)
#     for data in Data.objects.all():
#         writer.writerow(
#             [data.pk, data.period, data.experiment_number, data.user, data.question_number, data.judge, data.time,
#              data.correct,
#              data.answer])
#     return response
