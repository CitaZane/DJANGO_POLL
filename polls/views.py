from typing import Any
from django.db import models
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
# from django.template import loader
from django.urls import reverse
from django.utils import timezone

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future). If the request is made by admin, 
        include alsu unpublished questions.
        """
        if not self.request.user.is_staff:
            now = timezone.now()
            return Question.objects.filter(pub_date__lte=now,choice__isnull=False).order_by('-pub_date')[:5]
        return Question.objects.filter(choice__isnull=False).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    context_object_name = 'question' #custom context name

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet for reglar user.
        """
        if self.request.user.is_staff:
            return Question.objects.filter(choice__isnull=False)
        
        return Question.objects.filter(pub_date__lte=timezone.now(),choice__isnull=False)

    def get_context_data(self, **kwargs):
        """
        Add additional context to include the related choices
        for the question.
        """
        context = super().get_context_data(**kwargs)
        question = context['question']
        context['choices'] = question.choice_set.all()
        return context
    


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    def get_queryset(self):
        if self.request.user.is_staff:
            return Question.objects.filter( choice__isnull=False).distinct()
        return Question.objects.filter(pub_date__lte=timezone.now(), choice__isnull=False).distinct()
    

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
