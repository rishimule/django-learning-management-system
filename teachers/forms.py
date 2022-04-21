from accounts.models import Classroom,Teacher, Section, Resource,Assignment,AssignmentSubmission
from django import forms

class ClassroomForm(forms.ModelForm):
    
    class Meta:
        model = Classroom
        exclude = ('teacher',)

class SectionForm(forms.ModelForm):
    
    class Meta:
        model = Section
        # fields = '__all__'
        exclude = ("classroom",)

class ResourceForm(forms.ModelForm):
    
    class Meta:
        model = Resource
        # fields = '__all__'
        exclude = ("section",)

class AssignmentForm(forms.ModelForm):
    
    class Meta:
        model = Assignment
        exclude = ("section",)
        widgets = {
            'deadline' : forms.SelectDateWidget
        }

