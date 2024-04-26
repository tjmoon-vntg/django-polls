from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


### login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'polls:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'polls/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('polls:index')


### rest api
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
#from rest_framework import status
#from .models import Question, Choice


from rest_framework import viewsets

from .serializers import QuestionSerializer, ChoiceSerializer

#from django.views import generic

## request api and get json back

# class ApiIndexView(APIView):
#     def get(self, request):
#         q1 = Question.objects.all()
#         serializer = QuestionSerializer(q1, many=True)
#         return Response(serializer.data)
    
#     def post(self):
#         pass

# viewsets
class ApiIndexView(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    # def get(self, request):
    #     q1 = Question.objects.all()
    #     serializer = QuestionSerializer(q1, many=True)
    #     return Response(serializer.data)
    
    # def post(self):
    #     pass

# class questionList(APIView):
#     def get(self, request):
#         q1 = Questions.objects.all()
#         serializer = QuestionSerializer(q1, many=True)
#         return Response(serializer.data)
    
#     def post(self):
#         pass
    
    
# class choiceList(APIView):
#     def get(self, request):
#         c1 = Choice.objects.all()
#         serializer = ChoiceSerializer(c1, many=True)
#         return Response(serializer.data)
    
#     def post(self):
#         pass
    
    
