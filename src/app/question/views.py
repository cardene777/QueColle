from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.datastructures import MultiValueDictKeyError

from .models import QuestionCollection, Question, Data, QuestionSchedule
from django.views import generic
from .forms import QuestionCollectionForm, QuestionForm, QuestionScheduleForm
from typing import List
import random
import time
import csv
from datetime import datetime


def about_datas(start_date, start_time, end_date, end_time):
    split_start_date = str(start_date).split("-")
    split_start_time = str(start_time).split(":")
    split_end_date = str(end_date).split("-")
    split_end_time = str(end_time).split(":")
    start = datetime(int(split_start_date[0]), int(split_start_date[1]), int(split_start_date[2]),
                     int(split_start_time[0]), int(split_start_time[1]), int(split_start_time[2]))
    end = datetime(int(split_end_date[0]), int(split_end_date[1]), int(split_end_date[2]),
                   int(split_end_time[0]), int(split_end_time[1]), int(split_end_time[2]))
    if start <= datetime.now() <= end:
        return "ok"
    else:
        return "no"


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
        context["numbers"] = range(1, int(QuestionCollection.objects.get(collection=collection_name).numbers) + 1)
        context["number_data"]: list = []
        context["judges"]: list = []
        for index, number in enumerate(context["numbers"]):
            data = QuestionSchedule.objects.filter(collection=collection_name).filter(number=number)
            if data:
                start_date = data[0].start_date
                start_time = data[0].start_time
                end_date = data[0].end_date
                end_time = data[0].end_time
                judges: str = about_datas(start_date, start_time, end_date, end_time)
                context["judges"].append(judges)
                datas: list = [data[0].id, f"{start_date}-{start_time}", f"~{end_date}-{end_time}"]
                context["number_data"].append(datas)
                continue
            context["number_data"].append(data)
            context["judges"].append("no")
        context["judges"].reverse()
        return context


class QuestionCollectionUpdate(generic.UpdateView):
    template_name = "question/question_collection_update.html"
    model = QuestionCollection
    form_class = QuestionCollectionForm

    def get_context_data(self, **kwargs):
        context = super(QuestionCollectionUpdate, self).get_context_data()
        context["collection_id"] = QuestionCollection.objects.get(id=self.kwargs["pk"]).id
        return context


class QuestionUpdate(generic.UpdateView):
    template_name = "question/question_update.html"
    model = Question
    form_class = QuestionForm

    def get_context_data(self, **kwargs):
        context = super(QuestionUpdate, self).get_context_data()
        collection_name: str = Question.objects.get(id=self.kwargs["pk"]).collection
        context["collection_id"] = QuestionCollection.objects.get(collection=collection_name).id
        return context


class QuestionDelete(generic.DeleteView):
    template_name = "question/question_delete.html"
    model = Question
    success_url = reverse_lazy('question:home')

    def get_context_data(self, **kwargs):
        context = super(QuestionDelete, self).get_context_data()
        collection_name: str = Question.objects.get(id=self.kwargs["pk"]).collection
        context["collection_id"] = QuestionCollection.objects.get(collection=collection_name).id
        return context


def question_list(request, collection_id):
    questions = Question.objects.filter(collection=int(collection_id))
    params: dict = {
        "questions": questions,
        "collection_id": collection_id
    }
    return render(request, 'question/question_list.html', params)


def question(requests, collection_id):
    """
    random choice question
    :param requests: requests
    :param collection_id: int
    :return: html file with one questions
    """
    collection_name: str = QuestionCollection.objects.get(id=collection_id)
    if Question.objects.filter(collection=collection_name).count() == 0:
        params: dict = {
            "message": "not question"
        }
        return render(requests, 'question/error.html', params)
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

        # データ登録
        collection_name = QuestionCollection.objects.get(id=requests.POST["collection_id"])
        question_question = Question.objects.get(question=requests.POST["question"])
        data = Data(collection=collection_name, question=question_question, user=requests.POST["username"],
                    judge=judge, answer_time=int(answer_time), correct_answer=correct_answer, user_answer=user_answer)
        data.save()
        params: dict = {
            "questions": questions,
            "message": message,
            "judge": judge,
            "correct_answer": correct_answer,
            "collection_id": requests.POST["collection_id"]
        }
        return render(requests, 'question/question.html', params)


def export(request, collection_value):
    """
    data export csv file
    :param collection_value:
    :param request:
    :return: csv file
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    # HttpResponseオブジェクトはファイルっぽいオブジェクトなので、csv.writerにそのまま渡せます。
    writer = csv.writer(response)
    collection_id = QuestionCollection.objects.get(collection=collection_value).id
    writer.writerow(["pk", "問題集", "問題文", "問題群番号", "ユーザー", "正誤", "解答時間", "正解", "ユーザー解答"])
    for data in Data.objects.filter(collection=collection_id):
        writer.writerow(
            [data.pk, collection_value, data.question, data.number, data.user, data.judge, data.answer_time,
             data.correct_answer, data.user_answer])
    return response


class CreateQuestionCollection(generic.CreateView):
    template_name = "question/create_question_collection.html"
    model = QuestionCollection
    form_class = QuestionCollectionForm
    success_url = reverse_lazy("question:home")


def create_question(requests, question_collection_id):
    if requests.method == "POST":
        question_data = QuestionForm(requests.POST, instance=Question())
        question_data.save()
        question_collects = QuestionCollection.objects.filter(id=question_collection_id)[0]
        length: int = Question.objects.filter(collection=question_collection_id).count()
        params: dict = {
            "question_collection": question_collects,
            "length": length
        }
        return render(requests, 'question/question_about.html', params)
    form = QuestionForm()
    collection_name: str = QuestionCollection.objects.get(id=question_collection_id)
    params: dict = {
        "form": form,
        "collection_name": collection_name,
        "collection_id": question_collection_id
    }
    return render(requests, 'question/create_question.html', params)


def aggregation(requests, username):
    user_collections: list = list(QuestionCollection.objects.filter(user=username).values_list("collection", flat=True))
    if requests.method == "POST":
        user_collection = requests.POST["user_collection"]
        if user_collection == "None":
            params: dict = {
                "message": "no data",
                "user_collections": user_collections,
            }
            return render(requests, 'question/aggregation.html', params)
        collection_about = QuestionCollection.objects.filter(collection=user_collection)
        collection_value: str = collection_about.values_list("collection", flat=True)[0]
        about_value: str = collection_about.values_list("collection", flat=True)[0]
        attention_value: str = collection_about.values_list("attention", flat=True)[0]
        collection_data = Data.objects.filter(collection=list(collection_about.values_list("id", flat=True))[0])
        if not collection_data:
            params: dict = {
                "message": "no",
                "user_collections": user_collections,
            }
            return render(requests, 'question/aggregation.html', params)
        params: dict = {
            "message": "yes",
            "collection_about": collection_about,
            "collection_data": collection_data,
            "collection_value": collection_value,
            "about_value": about_value,
            "attention_value": attention_value,
            "user_collections": user_collections
        }
        return render(requests, 'question/aggregation.html', params)
    params: dict = {
        "user_collections": user_collections
    }
    return render(requests, 'question/aggregation.html', params)


def plot(request, username, collection):
    user_collections: list = list(QuestionCollection.objects.filter(user=username).values_list("collection", flat=True))
    collections = QuestionCollection.objects.get(collection=collection)
    collection_id: int = collections.id
    datas = Data.objects.filter(collection=collection_id)
    collection_number: int = collections.numbers
    collection_numbers: list = []
    collection_answer_time: list = []
    collection_judge: list = []
    for number in range(int(collection_number)):
        collection_numbers.append(datas.filter(number=number + 1))
        collection_answer_time.append(datas.filter(number=number + 1).values_list("answer_time", flat=True))
        collection_judge.append(datas.filter(number=number + 1).values_list("judge", flat=True))
    collection_number_list: list = ",".join(list(map(str, range(1, int(collection_number) + 1))))
    answer_time: list = []
    judges: list = []
    for time in collection_answer_time:
        if sum(list(time)) == 0:
            answer_time.append("0")
        else:
            answer_time.append(str(sum(list(time)) / 10))

    def change_judge(j):
        bool_dict: dict = {
            "正解": 1,
            "不正解": 0
        }
        change_j: int = bool_dict[j]
        return change_j

    for judge in collection_judge:
        judge = list(map(change_judge, judge))
        if len(judge) == 0:
            judges.append("0")
        else:
            judges.append(str((sum(judge) / len(judge)) * 100))
    answer_time = ",".join(answer_time)
    judges = ",".join(judges)

    collection_about = QuestionCollection.objects.filter(collection=collection)
    collection_value: str = collection_about.values_list("collection", flat=True)[0]
    about_value: str = collection_about.values_list("collection", flat=True)[0]
    attention_value: str = collection_about.values_list("attention", flat=True)[0]
    collection_data = Data.objects.filter(collection=list(collection_about.values_list("id", flat=True))[0])
    params: dict = {
        "message": "yes",
        "plot": "graph_on",
        "collection_number_list": collection_number_list,
        "answer_time": answer_time,
        "judges": judges,
        "collection_about": collection_about,
        "collection_data": collection_data,
        "collection_value": collection_value,
        "about_value": about_value,
        "attention_value": attention_value,
        "user_collections": user_collections,
    }
    return render(request, 'question/aggregation.html', params)


def schedule(request):
    if request.method == "POST":
        collection_id: int = request.POST["collection_id"]
        number: int = request.POST["number"]
        forms = QuestionScheduleForm()
        params: dict = {
            "collection_id": collection_id,
            "number": number,
            "forms": forms,
            "message": request.POST["message"]
        }
        return render(request, 'question/create_schedule.html', params)


def schedule_create(request):
    collection_id: int = request.POST["collection_id"]
    try:
        model = QuestionSchedule.objects.filter(
            collection=collection_id).filter(number=request.POST["number"])[0]
        data = QuestionScheduleForm(request.POST, instance=model)
    except:
        data = QuestionScheduleForm(request.POST, instance=QuestionSchedule())
    data.save()
    question_collects = QuestionCollection.objects.filter(id=collection_id)[0]
    length: int = Question.objects.filter(collection=collection_id).count()
    numbers: int = range(1, int(QuestionCollection.objects.get(id=collection_id).numbers) + 1)
    number_data: list = []
    judges: list = []
    for index, number in enumerate(numbers):
        data = QuestionSchedule.objects.filter(collection=collection_id).filter(number=number)
        if data:
            start_date = data[0].start_date
            start_time = data[0].start_time
            end_date = data[0].end_date
            end_time = data[0].end_time
            judge: str = about_datas(start_date, start_time, end_date, end_time)
            judges.append(judges)
            datas: list = [data[0].id, f"{start_date}-{start_time}", f"~{end_date}-{end_time}"]
            number_data.append(datas)
            continue
        number_data.append(data)
        judges.append("no")
    judges.reverse()
    params: dict = {
        "question_collection": question_collects,
        "length": length,
        "numbers": numbers,
        "number_data": number_data,
        "judges": judges
    }
    if request.POST["message"] == "update":
        questions_count = Question.objects.filter(collection=collection_id).count()
        collection_user: str = QuestionCollection.objects.filter(id=collection_id)[0].user
        params: dict = {
            "schedule": model,
            "questions_count": questions_count,
            "collection_id": collection_id,
            "collection_user": collection_user
        }
        return render(request, 'question/schedule_detail.html', params)
    return render(request, 'question/question_about.html', params)


def schedule_detail(request):
    schedule_id: str = request.POST["schedule_id"]
    schedule_id: int = int(schedule_id.replace("[", "").replace("]", ""))
    schedule = QuestionSchedule.objects.filter(id=schedule_id)[0]
    collection_id = request.POST["collection_id"]
    questions_count = Question.objects.filter(collection=collection_id).count()
    collection_user: str = QuestionCollection.objects.filter(id=collection_id)[0].user
    params: dict = {
        "schedule": schedule,
        "questions_count": questions_count,
        "collection_id": collection_id,
        "collection_user": collection_user
    }
    return render(request, 'question/schedule_detail.html', params)
