from django.http import HttpResponseRedirect
from django import forms
from django import views
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, DetailView
from accounts.models import Classroom,Teacher,User,Section, Resource,Assignment,AssignmentSubmission
from accounts.passtests import StudentTestMixin, TeacherTestMixin
from .forms import AssignmentSubmissionForm, JoinClassroomForm

# Create your views here.

class DashboardView(StudentTestMixin, TemplateView):
    template_name = "students/dashboard.html"

def ClassroomDetailView(request,code):
    context_dict = {}
    room = get_object_or_404(Classroom, code=code)
    context_dict['classroom'] = room
    return render(request, 'students/classroom_detail.html', context=context_dict)

def ResourcesView(request, pk):
    context_dict = {}
    section = get_object_or_404(Section, pk=pk)
    print(section)
    context_dict['section'] = section
    return render(request, 'students/resources.html', context=context_dict)

def AssignmentsView(request, pk):
    context_dict = {}
    section = get_object_or_404(Section, pk=pk)
    print(section)
    context_dict['section'] = section
    return render(request, 'students/assignments.html', context=context_dict)

class AssignmentSubmissionCreateView(CreateView):
    model = AssignmentSubmission
    form_class = AssignmentSubmissionForm
    template_name = "students/assignmentsubmission.html"

    def form_valid(self, form):
        form.instance.assignment = get_object_or_404(Assignment, pk=self.kwargs['pk'])
        form.instance.student = self.request.user.students
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('students:assignments', kwargs={'pk':Assignment.objects.get(pk=self.kwargs['pk']).section.pk})

def MyAssignmentView(request, pk):
    context_dict = {}
    student = request.user.students
    assignment = Assignment.objects.get(pk=pk)
    
    if AssignmentSubmission.objects.filter(assignment=assignment).filter(student=student).exists():
        context_dict['assignment'] = assignment
        context_dict['submission'] = AssignmentSubmission.objects.filter(assignment=assignment).filter(student=student)[0]
        context_dict['assignmentfilename'] = context_dict['submission'].file.name.split('/')[-1]
        return render(request, template_name='students/my_assignment.html', context=context_dict)
    else:
        return redirect('students:submit_assignment', pk=pk)

class AssignmentSubmissionDeleteView(DeleteView):
    model = AssignmentSubmission
    template_name = "students/deletesubmission.html"
    
    def get_success_url(self):
        return reverse('students:assignments', kwargs={'pk':self.object.assignment.section.pk})

def joinClassroomView(request):
    form = JoinClassroomForm()
    
    if request.method == 'POST':
        form = JoinClassroomForm(request.POST)
        
        if form.is_valid():
            code = form.cleaned_data['code']
            print(code)
            if Classroom.objects.filter(code=code).exists():
                print('Exists', form.cleaned_data['code'])
                
                if request.user.students.classrooms.filter(code=code).exists():
                    print('User already a member')
                    return HttpResponseRedirect(reverse('students:dashboard'))
                else:
                    print('User not a member')
                    request.user.students.classrooms.add(Classroom.objects.filter(code=code).first())
                    print('User joined the classroom')
                    return HttpResponseRedirect(reverse('students:dashboard')) 
            else:
                print('Classroom dosent exist')
    return render(request, 'students/join_classroom.html', {'form':form})


def LeaveClassroomView(request,code):
    request.user.students.classrooms.remove(Classroom.objects.filter(code=code).first())
    return HttpResponseRedirect(reverse('students:dashboard'))
    







