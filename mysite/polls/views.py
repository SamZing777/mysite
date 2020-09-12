from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse
from django.http import HttpResponse
from django.utils import timezone

from .models import Question, Choice


class IndexView(generic.ListView):
    model = Question
    context_object_name = 'latest_question_list'
    template_name = 'polls/index.html'
    
    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
        

 
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    
    def get_queryset(self):
        
        # excludes questions not published yet
        
        return Question.objects.filter(pub_date__lte=timezone.now())

"""
def index(request):
    
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, pk):
    return HttpResponse("you're looking at question %s." % question_id)
"""
