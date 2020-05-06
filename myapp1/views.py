from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import DetailView, UpdateView, CreateView, ListView, DeleteView
from .forms import UserForm, ListForm, CardForm, CardCreateFromHomeForm
from . models import List, Card
from .mixins import OnlyYouMixin

def index(request):
    return render(request, "myapp1/index.html") 

class HomeView(LoginRequiredMixin, ListView):
    model = List
    template_name = "myapp1/home.html"

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user_instance = form.save()
            login(request, user_instance)
            return redirect("myapp1:home")
    else:
        form = UserCreationForm()

    context = {
        "form": form
    }
    return render(request, 'myapp1/signup.html', context)

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "myapp1/users/detail.html"

class UserUpdateView(OnlyYouMixin, UpdateView):
    model = User
    template_name = "myapp1/users/update.html"
    form_class = UserForm

    def get_success_url(self):
        return resolve_url('myapp1:users_detail', pk=self.kwargs['pk'])

class ListCreateView(LoginRequiredMixin, CreateView):
    model = List
    template_name = "myapp1/lists/create.html"
    form_class = ListForm
    success_url = reverse_lazy("myapp1:lists_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ListListView(LoginRequiredMixin, ListView):
    model = List
    template_name = "myapp1/lists/list.html"

class ListDetailView(LoginRequiredMixin, DetailView):
    model = List
    template_name = "myapp1/lists/detail.html"

class ListUpdateView(LoginRequiredMixin, UpdateView):
    model = List
    template_name = "myapp1/lists/update.html"
    form_class = ListForm
    success_url = reverse_lazy("myapp1:home")

    def get_success_url(self):
        return resolve_url('myapp1:lists_detail', pk=self.kwargs['pk'])

class ListDeleteView(LoginRequiredMixin, DeleteView):
    model = List
    template_name = "myapp1/lists/delete.html"
    form_class = ListForm
    success_url = reverse_lazy("myapp1:home")

class CardCreateView(LoginRequiredMixin, CreateView):
    model = Card
    template_name = "myapp1/cards/create.html"
    form_class = CardForm
    success_url = reverse_lazy("myapp1:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CardListView(LoginRequiredMixin, ListView):
    model = Card
    template_name = "myapp1/cards/list.html"

class CardDetailView(LoginRequiredMixin, DetailView):
    model = Card
    template_name = "myapp1/cards/detail.html"

class CardUpdateView(LoginRequiredMixin, UpdateView):
    model = Card
    template_name = "myapp1/cards/update.html"
    form_class = CardForm
    success_url = reverse_lazy("myapp1:home")

    def get_success_url(self):
        return resolve_url('myapp1:cards_detail', pk=self.kwargs['pk'])

class CardDeleteView(LoginRequiredMixin, DeleteView):
    model = Card
    template_name = "myapp1/cards/delete.html"
    form_class = CardForm
    success_url = reverse_lazy("myapp1:home")

class CardCreateFromHomeView(LoginRequiredMixin, CreateView):
    model = Card
    template_name = "myapp1/cards/create.html" 
    form_class = CardCreateFromHomeForm
    success_url = reverse_lazy("myapp1:home")

    def form_valid(self, form):
        list_pk = self.kwargs['list_pk']
        list_instance = get_object_or_404(List, pk=list_pk)
        form.instance.list = list_instance
        form.instance.user = self.request.user
        return super().form_valid(form)