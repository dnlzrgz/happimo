from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from moods.models import Entry


class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
    context_object_name = "entries"
    template_name = "moods/entry_list.html"
    paginate_by = 45

    def get(self, request, *args, **kwargs):
        if request.headers.get("X-Next-Page"):
            self.template_name = "moods/hx_entry_list.html"

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return (
            Entry.objects.filter(user=self.request.user)
            .prefetch_related(
                "activities",
                "mood",
            )
            .only("mood", "note_title", "date", "time")
        )


class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    fields = ["mood", "activities", "note_title", "note_body", "date", "time"]
    slug_field = "sqid"
    template_name = "moods/entry_create_form.html"
    success_url = reverse_lazy("entry_list")

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy("home"))

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Entry
    template_name = "moods/entry_delete_form.html"
    slug_field = "sqid"
    success_url = reverse_lazy("entry_list")

    def test_func(self):
        return self.get_object().user == self.request.user

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy("home"))


class EntryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Entry
    fields = ["mood", "activities", "note_title", "note_body", "date", "time"]
    slug_field = "sqid"
    template_name = "moods/entry_update_form.html"
    success_url = reverse_lazy("entry_list")

    def test_func(self):
        return self.get_object().user == self.request.user

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy("home"))
