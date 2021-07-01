from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from .models import Question, Choice


class IndexView(generic.ListView):
    # ListView: <app name>/<model name>_list.html
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'  # same thing

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    # DetailView: <app name>/<model name>_detail.html
    model = Question  # need to know which model is acting upon
    template_name = 'polls/detail.html'  # specify the template


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # prevent data from being posted twice when user hits the back button
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
