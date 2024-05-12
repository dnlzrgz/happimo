from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from moods.models import Activity


class ActivityListView(LoginRequiredMixin, ListView):
    model = Activity
    context_object_name = "activities"
    template_name = "moods/activity_list.html"

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)


class ActivityCreateView(LoginRequiredMixin, CreateView):
    model = Activity
    fields = ["name"]
    slug_field = "sqid"
    template_name = "moods/activity_create_form.html"
    success_url = reverse_lazy("activity_list")

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy("home"))

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ActivityDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Activity
    template_name = "moods/activity_delete_form.html"
    slug_field = "sqid"
    success_url = reverse_lazy("activity_list")

    def test_func(self):
        return self.get_object().user == self.request.user

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy("home"))


class ActivityUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Activity
    fields = ["name"]
    slug_field = "sqid"
    template_name = "moods/activity_update_form.html"
    success_url = reverse_lazy("activity_list")

    def test_func(self):
        return self.get_object().user == self.request.user

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy("home"))
