from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import *
# Create your views here.



@method_decorator(login_required(login_url='registration:login'),name='dispatch')
class Dashboard(View):



    def get(self,request):

        types_obj = QuestionType.objects.all()
        subjects_obj = SubjectInfo.objects.all()

        return render(request,'dashboard/test.html',locals())

    def post(self,request):
        postdata = request.POST.copy()
        print(postdata)

        return render(request,'dashboard/test.html',locals())


