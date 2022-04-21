from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import CharField
from django.urls import reverse
from django.utils import timezone, text
from django.core.validators import MaxValueValidator, MinValueValidator
import os
import datetime
import random
import string


def _(something):
    return something


class User(AbstractUser):
    is_student = models.BooleanField('student status', default=False)
    is_teacher = models.BooleanField('teacher status', default=False)


class Stream(models.Model):

    name = models.CharField(
        _("Stream Name"),
        max_length=250,
        blank=False,
        unique=True)

    class Meta:
        verbose_name = _("stream")
        verbose_name_plural = _("streams")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("stream_detail", kwargs={"pk": self.pk})


class Class(models.Model):

    stream = models.ForeignKey(
        "Stream",
        on_delete=models.CASCADE,
        related_name="classes",
        blank=False)

    name = models.CharField(
        _("Class Name"),
        max_length=250,
        blank=False,
        unique=True)

    semester = models.PositiveIntegerField(
        blank=False,
        default=1,
        validators=[
            MaxValueValidator(8),
            MinValueValidator(1)
        ]
    )

    year = models.PositiveIntegerField(
        blank=False,
        default=2022,
        validators=[
            MaxValueValidator(2030),
            MinValueValidator(2015)
        ]
    )

    class Meta:
        verbose_name = _("class")
        verbose_name_plural = _("classes")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("class_detail", kwargs={"pk": self.pk})


class Teacher(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='teachers')

    stream = models.ForeignKey(
        "Stream",
        on_delete=models.CASCADE,
        related_name="teachers",
        blank=False)

    class Meta:
        verbose_name = _("teacher")
        verbose_name_plural = _("teachers")

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("teacher_detail", kwargs={"pk": self.pk})

def random_string(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Classroom(models.Model):

    teacher = models.ForeignKey(
        "Teacher",
        on_delete=models.CASCADE,
        blank=False,
        related_name='classrooms')

    subject = models.CharField(
        _("Subject Name"),
        max_length=50,
        blank=False)

    code = models.SlugField(
        _("Subject Code"),
        max_length=10,
        default=random_string,
        unique=True)

    semester = models.PositiveIntegerField(
        blank=False,
        default=1,
        validators=[
            MaxValueValidator(8),
            MinValueValidator(1)
        ]
    )

    created_timestamp = models.DateTimeField(
        default=timezone.now,
        editable=False)

    class Meta:
        verbose_name = _("Classroom")
        verbose_name_plural = _("Classrooms")

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse("Classroom_detail", kwargs={"pk": self.pk})


class Student(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='students')

    current_class = models.ForeignKey(
        "Class",
        verbose_name=_("Class"),
        on_delete=models.CASCADE,
        blank=False,
        related_name='students')

    roll_no = models.PositiveIntegerField(
        _("Roll No."),
        blank=False)

    student_id = models.CharField(
        _("Student ID"),
        max_length=50,
        blank=False,
        unique=True)

    classrooms = models.ManyToManyField("Classroom", related_name='students', blank=True)
    
    class Meta:
        verbose_name = _("student")
        verbose_name_plural = _("students")
        unique_together = ('roll_no', 'current_class')

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("Student_detail", kwargs={"pk": self.pk})


class Section(models.Model):

    classroom = models.ForeignKey(
        "Classroom",
        on_delete=models.CASCADE,
        blank=False,
        related_name='sections')

    title = models.CharField(
        _("section title"),
        max_length=150)

    created_timestamp = models.DateTimeField(
        default=timezone.now,
        editable=False
    )

    class Meta:
        verbose_name = _("section")
        verbose_name_plural = _("sections")

    def __str__(self):
        return f'{self.title} -> {self.classroom.subject}'

    def get_absolute_url(self):
        return reverse("section_detail", kwargs={"pk": self.pk})


def resource_rename_upload_file(instance, filename):
    ogfilename = filename.rsplit('.', 1)[0]
    ext = filename.split('.')[-1]
    filename = f'{text.slugify(instance.section.classroom)}/{text.slugify(instance.section)}/{text.slugify(instance.title)}/{text.slugify(instance.created_timestamp)}/{text.slugify(ext)}/{text.slugify(filename)}/{text.slugify(ogfilename)}.{text.slugify(ext)}' 
    print(filename)
    return os.path.join('files/resources/', filename)


class Resource(models.Model):

    title = models.CharField(
        _("resource title"),
        max_length=150)

    created_timestamp = models.DateTimeField(
        default=timezone.now,
        editable=False
    )

    text = models.TextField()

    section = models.ForeignKey(
        "Section",
        on_delete=models.CASCADE,
        related_name='resources',
        blank=False)

    file = models.FileField(
        upload_to=resource_rename_upload_file,
        blank=True,
        max_length=999)

    class Meta:
        verbose_name = _("resource")
        verbose_name_plural = _("resources")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("resource_detail", kwargs={"pk": self.pk})


def assignment_rename_upload_file(instance, filename):
    ogfilename = filename.rsplit('.', 1)[0]
    ext = filename.split('.')[-1]
    filename = f'{text.slugify(instance.section.classroom)}/{text.slugify(instance.section)}/{text.slugify(instance.title)}/{text.slugify(instance.created_timestamp)}/{text.slugify(ext)}/{text.slugify(filename)}/{text.slugify(ogfilename)}.{text.slugify(ext)}'
    print(filename)
    return os.path.join('files/assignments/', filename)


class Assignment(models.Model):

    title = models.CharField(
        _("section title"),
        max_length=150)

    section = models.ForeignKey(
        "Section",
        on_delete=models.CASCADE,
        related_name='assignments',
        blank=False)

    text = models.TextField()

    created_timestamp = models.DateTimeField(
        default=timezone.now,
        editable=False
    )

    deadline = models.DateTimeField(
        default=timezone.now,
        blank=False
    )

    file = models.FileField(
        upload_to=assignment_rename_upload_file,
        blank=True,
        max_length=999)

    class Meta:
        verbose_name = _("assignment")
        verbose_name_plural = _("assignments")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("assignment_detail", kwargs={"pk": self.pk})


def submission_rename_upload_file(instance, filename):
    ogfilename = filename.rsplit('.', 1)[0]
    ext = filename.split('.')[-1]
    filename = f'{text.slugify(instance.assignment.section.classroom)}/{text.slugify(instance.assignment.section)}/{text.slugify(instance.assignment.title)}/{text.slugify(instance.student)}/{text.slugify(ext)}/{text.slugify(filename)}/{text.slugify(ogfilename)}.{text.slugify(ext)}'
    print(filename)
    return os.path.join('files/assignment_submission/', filename)



class AssignmentSubmission(models.Model):

    student = models.ForeignKey(
        "Student", 
        verbose_name=_("Submitted by"), 
        on_delete=models.CASCADE, 
        related_name='assignment_submissions',
        blank=False)
    
    assignment = models.ForeignKey(
        "Assignment", 
        on_delete=models.CASCADE,
        related_name='assignment_submissions',
        blank=False)

    file = models.FileField(
        upload_to=submission_rename_upload_file,
        blank=False,
        max_length=999)

    submission_timestamp = models.DateTimeField(
        default=timezone.now,
        editable=False
    )
    
    class Meta:
        verbose_name = _("assignmentsubmission")
        verbose_name_plural = _("assignmentsubmissions")
        unique_together = ('student', 'assignment')

    def __str__(self):
        return f'{self.assignment} -> {self.student}'

    def get_absolute_url(self):
        return reverse("assignmentsubmission_detail", kwargs={"pk": self.pk})

