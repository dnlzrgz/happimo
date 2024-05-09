from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from moods.models import Mood


class MoodListView(LoginRequiredMixin, ListView):
    model = Mood
    context_object_name = "moods"
    template_name = "moods/mood_list.html"
    ordering = ["name"]

    def get_queryset(self):
        return Mood.objects.filter(user=self.request.user)


class MoodCreateView(LoginRequiredMixin, CreateView):
    model = Mood
    fields = ["icon", "name"]
    slug_field = "sqid"
    template_name = "moods/mood_create_form.html"
    success_url = reverse_lazy("home")

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy("home"))

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MoodDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mood
    template_name = "moods/mood_delete_form.html"
    slug_field = "sqid"
    success_url = reverse_lazy("home")

    def test_func(self):
        return self.get_object().user == self.request.user

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy("home"))


class MoodUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mood
    fields = ["icon", "name"]
    slug_field = "sqid"
    template_name = "moods/mood_update_form.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        return self.get_object().user == self.request.user

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy("home"))
