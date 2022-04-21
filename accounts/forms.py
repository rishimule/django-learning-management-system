from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Student, User, Teacher, Class, Classroom
 

class StudentForm(UserCreationForm):
    def __init__(self,*args,**kwargs):
        self.stream = kwargs.pop('stream')
        print('stream is ', self.stream)
        super(StudentForm,self).__init__(*args,**kwargs)
        
        if Class.objects.all().exists():
            self.fields['current_class'].queryset = Class.objects.filter(stream=self.stream).order_by('name')

    email = forms.EmailField(label='Email', required=True)
    
    first_name = forms.CharField(
        label='First Name', max_length=250, required=True)
    
    last_name = forms.CharField(
        label='Last Name', max_length=250, required=True)
    
    current_class = forms.ModelChoiceField(queryset=None, empty_label=None, required=True)
    
    roll_no =forms.IntegerField(label='Roll No.', required=True, min_value=1, max_value=500)
    
    student_id = forms.CharField(label='Student ID', max_length=50, required=True, min_length=4)
    
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        student = Student.objects.create(
            user=user,
            current_class = self.cleaned_data['current_class'],
            roll_no = self.cleaned_data['roll_no'],
            student_id = self.cleaned_data['student_id'],   
            )
        student.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        current_class = cleaned_data.get('current_class')
        roll_no = self.cleaned_data.get('roll_no')
        student_id = self.cleaned_data.get('student_id')
        email = self.cleaned_data.get('email')
        
        # Class and Roll No. Unique Constraint Validation
        if Student.objects.filter(current_class=current_class).filter(roll_no=roll_no).exists():
            print("Roll no in class")
            raise forms.ValidationError('Student with Roll No. already exists.')
        
        # Student id validation
        if Student.objects.filter(student_id=student_id).exists():
            print("Student ID exists")
            raise forms.ValidationError('Student with Student ID already exists.')
        
        # Email Validations
        if User.objects.filter(email=email).exists():
            print("Email exists")
            raise forms.ValidationError('User with Email already exists.')


class TeacherForm(UserCreationForm):
    def __init__(self,*args,**kwargs):
        self.stream = kwargs.pop('stream')
        print('stream is ', self.stream)
        print(type(self.stream))
        super(TeacherForm,self).__init__(*args,**kwargs)

    email = forms.EmailField(label='Email', required=True)
    
    first_name = forms.CharField(
        label='First Name', max_length=250, required=True)
    
    last_name = forms.CharField(
        label='Last Name', max_length=250, required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        teacher = Teacher.objects.create(
            user=user,
            stream = self.stream   
            )
        teacher.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        email = self.cleaned_data.get('email')

        # Email Validations
        if User.objects.filter(email=email).exists():
            print("Email exists")
            raise forms.ValidationError('User with Email already exists.')
                