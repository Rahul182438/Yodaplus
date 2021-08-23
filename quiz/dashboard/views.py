from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .models import *
# Create your views here.



class Dashboard(View):

    types_obj = QuestionType.objects.all()
    subjects_obj = SubjectInfo.objects.all()

    def get(self,request):


        return render(request,'dashboard/test.html',locals())

    def post(self,request):
        postdata = request.POST.copy()
        print(postdata)

        return render(request,'dashboard/test.html',locals())


