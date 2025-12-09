from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    return render(request, "learning_logs/index.html")

class TopicList(LoginRequiredMixin, ListView):
    model = Topic
    template_name = "learning_logs/topics.html"
    context_object_name = "topics"

    def get_queryset(self):
        return Topic.objects.filter(owner=self.request.user)

class TopicDetail(LoginRequiredMixin, DetailView):
    model = Topic
    template_name = "learning_logs/topic.html"
    context_object_name = "topic"

    def get_queryset(self):
        return Topic.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entries"] = Entry.objects.filter(topic=self.object).order_by("-date_added")
        return context

class TopicCreate(LoginRequiredMixin, CreateView):
    model = Topic
    template_name = "learning_logs/new_topic.html"
    form_class = TopicForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class TopicEdit(LoginRequiredMixin, UpdateView):
    model = Topic
    template_name = "learning_logs/edit_topic.html"
    form_class = TopicForm
    context_object_name = "topic"
    pk_url_kwarg = "topic_id"

    def get_queryset(self):
        return Topic.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse("topic", args=[self.object.id])

class TopicDelete(LoginRequiredMixin, DeleteView):
    model = Topic
    template_name = "learning_logs/delete_topic.html"
    context_object_name = "topic"
    pk_url_kwarg = "topic_id"

    def get_success_url(self):
        return reverse("topics")

class EntryCreate(LoginRequiredMixin, CreateView):
    model = Entry
    template_name = "learning_logs/new_entry.html"
    form_class = EntryForm

    def dispatch(self, request, *args, **kwargs):
        self.topic = get_object_or_404(Topic, pk=kwargs["topic_id"])
        if self.topic.owner != request.user:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topic"] = self.topic
        return context

    def form_valid(self, form):
        form.instance.topic = self.topic
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("topic", args=[self.topic.id])

class EntryEdit(LoginRequiredMixin, UpdateView):
    model = Entry
    template_name = "learning_logs/edit_entry.html"
    form_class = EntryForm
    context_object_name = "entry"
    pk_url_kwarg = "entry_id"

    def get_queryset(self):
        return Entry.objects.filter(topic__owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topic"] = self.object.topic
        return context

    def get_success_url(self):
        return reverse("topic", args=[self.object.topic.id])

class EntryDelete(LoginRequiredMixin, DeleteView):
    model = Entry
    template_name = "learning_logs/delete_entry.html"
    context_object_name = "entry"
    pk_url_kwarg = "entry_id"

    def get_queryset(self):
        return Entry.objects.filter(topic__owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topic"] = self.object.topic
        return context

    def get_success_url(self):
        return reverse("topic", args=[self.object.topic.id])
