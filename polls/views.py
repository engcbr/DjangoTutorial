from django.shortcuts import render, get_object_or_404

from django.http import HttpResponseRedirect, HttpResponse
from .models import Question, Choice
from django.template import loader
from django.http import Http404
from django.core.urlresolvers import reverse
from django.views import generic

# def index(request):
#     print "Enter Index Function"
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     print latest_question_list
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     print "Exit Index Function"
#     return HttpResponse(template.render(context, request))
#     #return render(request, 'polls/index.html', context)
#
#
# def detail(request, question_id):
#     print "Enter Detail Function"
#     try:
#         question = Question.objects.get(pk=question_id)
#         print question
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     print "Exit Detail Function"
#     return render(request, 'polls/detail.html', {'question': question})
#     #question = get_object_or_404(Question, pk=question_id)
#     #return render(request, 'polls/detail.html', {'question': question})
#
#
# def results(request, question_id):
#     print "Enter Results Function"
#     question = get_object_or_404(Question, pk=question_id)
#     print "Exit Results Function"
#     return render(request, 'polls/results.html', {'question': question})

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'



def vote(request, question_id):
    print "Enter Vote Function"
    question = get_object_or_404(Question, pk=question_id)
    print question
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        print "question.choice_set: ", question.choice_set
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        print "Exit Vote Function"
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
