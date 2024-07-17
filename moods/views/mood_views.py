from django.shortcuts import render
from django.db import models
from django.urls import reverse_lazy
from django.db.models import Case, When, F
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.views import View
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

    def get_queryset(self):
        return Mood.objects.filter(user=self.request.user)


class MoodCreateView(LoginRequiredMixin, CreateView):
    model = Mood
    fields = ["color", "name"]
    slug_field = "sqid"
    template_name = "moods/mood_create_form.html"
    success_url = reverse_lazy("mood_list")

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy("home"))

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MoodDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mood
    template_name = "moods/mood_delete_form.html"
    slug_field = "sqid"
    success_url = reverse_lazy("mood_list")

    def test_func(self):
        return self.get_object().user == self.request.user

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy("home"))


class MoodUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mood
    fields = ["color", "name"]
    slug_field = "sqid"
    template_name = "moods/mood_update_form.html"
    success_url = reverse_lazy("mood_list")

    def test_func(self):
        return self.get_object().user == self.request.user

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy("home"))


class MoodReorderView(LoginRequiredMixin, View):
    def post(self, request):
        if request.headers.get("HX-REQUEST"):
            new_mood_order = request.POST.getlist("mood")
            Mood.objects.filter(user=request.user, sqid__in=new_mood_order).update(
                relative_order=Case(
                    *[
                        When(sqid=sqid, then=i + 1)
                        for i, sqid in enumerate(new_mood_order)
                    ],
                    default=F("relative_order"),
                    output_field=models.PositiveSmallIntegerField(),
                )
            )

            moods = Mood.objects.filter(user=request.user)
            context = {"moods": moods}
            return render(request, "moods/hx_mood_list.html", context)
        else:
            return HttpResponseBadRequest()

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy("home"))
