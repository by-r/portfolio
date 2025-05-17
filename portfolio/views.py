from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Experience, Profile, Project, SkillCategory

# Create your views here.


class ProfileView(TemplateView):
    template_name = "portfolio/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = Profile.objects.first()

        context["profile"] = profile
        context["experiences"] = Experience.objects.filter(profile=profile)
        context["skills"] = SkillCategory.objects.all()
        context["projects"] = Project.objects.all()
        return context
