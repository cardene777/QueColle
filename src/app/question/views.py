from django.shortcuts import render
from .models import QuestionCollection, Question
from django.views import generic
from typing import List
import random


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
    # ランダムに問題を取得
    collection_name: str = QuestionCollection.objects.get(id=collection_id)
    questions: List[int] = list(Question.objects.filter(collection=collection_name).values_list("id", flat=True))
    one_question: int = random.choice(questions)
    questions.remove(one_question)
    one_questions: dict = Question.objects.get(id=one_question)
    # 問題番号取得
    question_counts: int = Question.objects.filter(collection=collection_name).count()
    question_number: int = question_counts - len(questions)
    params: dict = {
        "questions": questions,
        "one_questions": one_questions,
        "question_number": question_number
    }
    return render(requests, 'question/question.html', params)


def answer(requests):
    if requests.method == "POST":
        message: str = "answer"
        judge: str = "bad"
        questions: str = requests.POST["questions"]
        question_id: int = requests.POST["question_id"]
        user_answer: str = requests.POST["answer"]
        correct_answer: str = Question.objects.get(id=question_id)
        if str(correct_answer) == str(user_answer):
            judge: str = "good"

        params: dict = {
            "message": message,
            "judge": judge,
            "correct_answer": correct_answer,
        }
        return render(requests, 'question/question.html', params)

