from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from django.contrib.auth import login
from .models import Task
# Create your views here.

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'todo/task_list.html'
    context_object_name = 'task-list'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['task-list'] = context['task-list'].filter(user=self.request.user)
        context['count'] = context['task-list'].filter(complete=False).count()
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['task-list'] = context['task-list'].filter(title__icontains = search_input)
            context['search_input'] = search_input
        return context
         
class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'todo/task_detail.html'
    
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description' ]
    template_name = 'todo/task_form.html'    
    success_url = reverse_lazy('task-list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)
    
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('task-list')
    
    
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task-list')
    
class CustomLoginView(LoginView):
    template_name = 'todo/login.html'   
    fields = '__all__'
    redirect_authenticated_user = False
    
    def get_success_url(self):
        return reverse_lazy('task-list')
    
    
class RegisterationView(FormView):
    template_name = 'todo/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task-list')    
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterationView, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task-list')
        return super(RegisterationView, self).get(*args, **kwargs) 