from django.views.generic.base import TemplateView
from django.shortcuts import redirect


class HomePageView(TemplateView):
    template_name = "pages/home.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("entry_list")

        return super().dispatch(request, *args, **kwargs)
