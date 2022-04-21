from django.contrib import admin

from .models import (
                    User,
                    Stream,
                    Class,
                    Teacher,
                    Classroom,
                    Student,
                    Section,
                    Resource,
                    Assignment,
                    AssignmentSubmission            
                )
# Register your models here.

admin.site.register(User)
admin.site.register(Stream)
admin.site.register(Class)
admin.site.register(Teacher)
admin.site.register(Classroom)
admin.site.register(Student)
admin.site.register(Section)
admin.site.register(Resource)
admin.site.register(Assignment)
admin.site.register(AssignmentSubmission)

