from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from .views import IndexView, StudentCreateView, StreamView, TeacherCreateView
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'accounts'

urlpatterns = [
    path('', IndexView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='accounts/login.html',redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('signup/student/stream/', StreamView.as_view(template_name = "accounts/student_stream.html"), name='student_stream'),
    path('signup/student/<int:stream_pk>/', StudentCreateView.as_view(), name='student_signup'),
    
    path('signup/teacher/stream/', StreamView.as_view(template_name = "accounts/teacher_stream.html"), name='teacher_stream'),
    path('signup/teacher/<int:stream_pk>/', TeacherCreateView.as_view(), name='teacher_signup'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
