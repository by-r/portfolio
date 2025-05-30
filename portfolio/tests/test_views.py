from django.test import TestCase
from django.urls import reverse

from portfolio.models import Experience, Profile, Project, Skill, SkillCategory


class ProfileViewTests(TestCase):

    def setUp(self):
        self.profile = Profile.objects.create(
            name="John Doe",
            title="Software Engineer",
            about_text="Test about text",
            email="john@example.com",
            linkedin_url="https://linkedin.com/in/johndoe",
        )

    def test_profile_view(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "portfolio/profile.html")
        self.assertContains(response, self.profile.name)
        self.assertContains(response, self.profile.title.upper())


class ExperienceViewTests(TestCase):

    def setUp(self):
        self.profile = Profile.objects.create(
            name="John Doe",
            title="Software Engineer",
            email="john@example.com",
            linkedin_url="https://linkedin.com/in/johndoe",
        )
        self.experience = Experience.objects.create(
            profile=self.profile,
            position="Software Developer",
            company="Tech Corp",
            company_url="https://techcorp.com",
            start_date_month="1",
            start_date_year="2023",
            description="Test description",
        )

    def test_experience_display(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.experience.position)
        self.assertContains(response, self.experience.company)


class SkillViewTests(TestCase):

    def setUp(self):
        self.category = SkillCategory.objects.create(name="Programming", order=1)
        self.skill = Skill.objects.create(category=self.category, name="Python")

    def test_skills_display(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.name)
        self.assertContains(response, self.skill.name)

    def test_skills_ordering(self):
        category2 = SkillCategory.objects.create(name="Frameworks", order=2)
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        content = str(response.content)
        self.assertTrue(content.index(self.category.name) < content.index(category2.name))


class ProjectViewTests(TestCase):

    def setUp(self):
        self.profile = Profile.objects.create(
            name="John Doe",
            title="Software Engineer",
            email="john@example.com",
            linkedin_url="https://linkedin.com/in/johndoe",
        )
        self.category = SkillCategory.objects.create(name="Programming", order=1)
        self.skill = Skill.objects.create(category=self.category, name="Python")
        self.project = Project.objects.create(
            name="Test Project",
            description="A test project",
            github_url="https://github.com/test/project",
            live_url="https://project.example.com",
        )
        self.project.tags.add(self.skill)

    def test_project_display(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.name)
        self.assertContains(response, self.project.description)
        self.assertContains(response, self.project.github_url)
        self.assertContains(response, self.project.live_url)
        self.assertContains(response, self.skill.name)

    def test_multiple_projects(self):
        project2 = Project.objects.create(name="Another Project", description="Another test project")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.name)
        self.assertContains(response, project2.name)
