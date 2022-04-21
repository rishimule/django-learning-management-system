from accounts.models import Classroom,Teacher, Section, Resource,Assignment,AssignmentSubmission
from django import forms

class AssignmentSubmissionForm(forms.ModelForm):
    
    class Meta:
        model = AssignmentSubmission
        fields = ("file",)

class JoinClassroomForm(forms.Form):
    code = forms.CharField(max_length=50, required=True)
    

    
