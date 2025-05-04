from django.test import TestCase
from django.core.exceptions import ValidationError
from portfolio.models import Profile, Experience, SkillCategory, Skill


class ProfileModelTests(TestCase):
    def setUp(self):
        self.profile_data = {
            "name": "John Doe",
            "title": "Software Engineer",
            "about_text": "Test about text",
            "email": "john@example.com",
            "linkedin_url": "https://linkedin.com/in/johndoe",
        }

    def test_profile_creation(self):
        profile = Profile.objects.create(**self.profile_data)
        self.assertEqual(profile.name, "John Doe")
        self.assertEqual(profile.title, "SOFTWARE ENGINEER")

    def test_single_profile_constraint(self):
        Profile.objects.create(**self.profile_data)
        with self.assertRaises(ValidationError):
            Profile.objects.create(**self.profile_data)


class ExperienceModelTests(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create(
            name="John Doe",
            title="Software Engineer",
            email="john@example.com",
            linkedin_url="https://linkedin.com/in/johndoe",
        )
        self.experience_data = {
            "profile": self.profile,
            "position": "Software Developer",
            "company": "Tech Corp",
            "company_url": "https://techcorp.com",
            "start_date_month": "1",
            "start_date_year": "2023",
            "description": "Test description",
        }

    def test_experience_creation(self):
        experience = Experience.objects.create(**self.experience_data)
        self.assertEqual(experience.position, "Software Developer")
        self.assertEqual(experience.company, "Tech Corp")

    def test_experience_str_method(self):
        experience = Experience.objects.create(**self.experience_data)
        self.assertEqual(str(experience), "Software Developer")


class SkillCategoryModelTests(TestCase):
    def test_category_creation(self):
        category = SkillCategory.objects.create(name="Programming", order=1)
        self.assertEqual(str(category), "Programming")

    def test_category_ordering(self):
        category2 = SkillCategory.objects.create(name="Frameworks", order=2)
        category1 = SkillCategory.objects.create(name="Programming", order=1)
        categories = SkillCategory.objects.all()
        self.assertEqual(categories[0], category1)
        self.assertEqual(categories[1], category2)


class SkillModelTests(TestCase):
    def setUp(self):
        self.category = SkillCategory.objects.create(name="Programming", order=1)

    def test_skill_creation(self):
        skill = Skill.objects.create(category=self.category, name="Python")
        self.assertEqual(str(skill), "Python")
        self.assertEqual(skill.category, self.category)
