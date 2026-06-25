from django.shortcuts import get_object_or_404, render
from django.db.models import F
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Choice, Question

# Create your views here.
def index(request):
    
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # template = loader.get_template("polls/index.html")
    context = {"latest_question_list": latest_question_list}
    # return HttpResponse(template.render(context))
    return render(request,"polls/index.html",context)

def detail(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    # return HttpResponse("Youre looking for question %s" % question_id)
    return render(request, "polls/detail.html", {"question":question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})
    # response = "You're looking at the results of question: %s" % question_id
    # return HttpResponse(response)

def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay voting form
        return render(request,"polls/detail.html",{"question":question,"error_message":"You didnt select a choice"})
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    return HttpResponse("Youre voting on question %s" % question_id)

