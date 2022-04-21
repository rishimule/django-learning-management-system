from django.shortcuts import redirect, render
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.decorators import login_required, user_passes_test


class HomeView(TemplateView):
    template_name = "mylms/home.html"

@login_required
def DashboardView(request):
    if request.user.is_student:
        return redirect('students:dashboard')
    if request.user.is_teacher:
        return redirect('teachers:dashboard')
    if request.user.is_superuser:
        return redirect('admin:index')