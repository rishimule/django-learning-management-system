from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.views.generic import TemplateView, CreateView, ListView
from .models import User, Student, Teacher, Stream
from .forms import StudentForm, TeacherForm
from accounts.passtests import StudentTestMixin, TeacherTestMixin


# Create your views here.

class IndexView(TemplateView):
    template_name = "accounts/index.html"


class StudentCreateView(CreateView):
    model = User
    form_class = StudentForm
    template_name = "accounts/student_signup.html"

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('dashboard')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        print(self.kwargs)
        kwargs.update({
        'stream': Stream.objects.filter(pk=self.kwargs['stream_pk']).first(),
        })
        print(Stream.objects.filter(pk=self.kwargs['stream_pk']).first())
        return kwargs    

class StreamView(TemplateView):
    
    def get_context_data(self, **kwargs):
        context = super(StreamView, self).get_context_data(**kwargs)
        context['stream_list'] = Stream.objects.all()
        print   
        return context

class TeacherCreateView(CreateView):
    model = User
    form_class = TeacherForm
    template_name = "accounts/teacher_signup.html"

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('dashboard')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        print(self.kwargs)
        kwargs.update({
        'stream': Stream.objects.filter(pk=self.kwargs['stream_pk']).first(),
        })
        print(Stream.objects.filter(pk=self.kwargs['stream_pk']).first())
        return kwargs    