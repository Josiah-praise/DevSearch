from django.test import TestCase, SimpleTestCase, Client, RequestFactory
from django.urls import reverse, resolve
from .views import Project_List, Project_Detail
from .models import Project


class TestUrls(TestCase):
    '''
    Tests all the urls in the projects app
    tests for correct status codes
    tests for proper view resolution
    '''

    def setUp(self) -> None:
        # create a new project
        self.new_project = Project.objects.create(title="New Project", description="Test Project for project_detail url test")
        self.new_project_id = self.new_project.id


    def tearDown(self) -> None:
        # reset the database
        self.new_project.delete()
        self.new_project_id = None


    def test_project_list_url_is_OK(self):
        url = reverse('projects:project_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_project_list_url_is_resolved(self):
        view = resolve(reverse("projects:project_list"))
        self.assertEqual(view.func.__name__, Project_List.as_view().__name__)


    def test_project_detail_url_is_OK(self):
        url = reverse('projects:project_detail', args=(self.new_project_id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_project_detail_url_is_resolved(self):
        view = resolve(reverse("projects:project_detail", args=(self.new_project_id,)))
        self.assertEqual(view.func.__name__, Project_Detail.as_view().__name__)


    def test_wrong_url(self):
        url = 'nasdaq'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TestViews(TestCase):
    '''
    tests that the views return the right templates
    tests that views perform the expected logic
    '''

    def setUp(self) -> None:
        self.new_project = Project.objects.create(title="New Project", description="Test Project for project_detail url test")
        self.new_project_id = self.new_project.id

    def tearDown(self) -> None:
        self.new_project.delete()
        self.new_project_id = None

    def test_project_list_view_template(self):
        url = reverse('projects:project_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'projects/project_list.html')


    def test_project_list_view_logic(self):
            response = self.client.get(reverse('projects:project_list'))
            query_set = Project_List.get_queryset(self)
            self.assertQuerySetEqual(response.context["projects"], query_set)
    
    def test_project_detail_view_template(self):
        url = reverse('projects:project_detail', args=(self.new_project_id,))
        response = self.client.get(url)
        self.assertTemplateUsed(response, "projects/project_detail.html")