from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class NameView(TemplateView):
    template_name = "portfolio/landing.html"
