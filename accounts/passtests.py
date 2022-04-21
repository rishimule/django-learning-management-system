from django.contrib.auth.mixins import UserPassesTestMixin

class StudentTestMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.is_student
        else:
            return False
    
class TeacherTestMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.is_teacher
        else:
            return False