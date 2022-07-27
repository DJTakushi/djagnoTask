from django.test import TestCase
from django.test import Client
from django.test.utils import setup_test_environment
from django.urls import reverse
from .models import todo, todoManager


class index(TestCase):
    def test_basicPage(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 404)
        response = client.get(reverse('djangoTask:index'))
        self.assertEqual(response.status_code, 200)
        rContent = response.content.decode("utf-8")
        self.assertIs("<title>Todo Index</title>" in rContent, True)
        self.assertIs("<p>No todos are available.</p>" in rContent, True)

        # no table if no todos exist
        self.assertIs("</table>" in rContent, False)


    def test_todosInIndex(self):
        """ create 99 todos and check that they're all in the table """
        todoDict = {}
        for i in range(1,100):
            todoDict['title']="testTitle"+str(i)
            todo.objects.create_todo(todoDict)
        client = Client()
        response = client.get(reverse('djangoTask:index'))
        rContent = response.content.decode("utf-8")
        self.assertTrue("</table>" in rContent)
        for i in range(1,100):
            testString = "<a href=\"/todo/"+str(i)+"/\">testTitle"+str(i)+"</a>"
            self.assertTrue(testString in rContent)

class new(TestCase):
    def test_basicPage(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 404)
        response = client.get(reverse('djangoTask:new'))
        self.assertEqual(response.status_code, 200)
        rContent = response.content.decode("utf-8")
        self.assertIs("<h1>NEW</h1>" in rContent, True)
        self.assertIs("</table>" in rContent, True)
        self.assertIs("<td>Title</td>" in rContent, True)
        self.assertIs("<td>Description</td>" in rContent, True)
        self.assertIs("<td>Creation Date</td>" in rContent, True)
        self.assertIs("<td>Due Date</td>" in rContent, True)
        self.assertIs("<td>Status</td>" in rContent, True)
        self.assertIs("<td>Tags</td>" in rContent, True)

        self.assertTrue("<input type=\"text\" name=\"title\" id=\"title\" value=\"NEW\">" in rContent)
        self.assertTrue("<input type=\"text\" name=\"descriptionPost\"" in rContent)
        self.assertTrue("<input type=\"datetime-local\" name=\"creationDatePost\"" in rContent)
        self.assertTrue("<input type=\"datetime-local\" name=\"dueDatePost\"" in rContent)
        self.assertTrue("<input type=\"datetime-local\" name=\"dueDatePost\"" in rContent)
        self.assertTrue("<input type=\"text\" name=\"statusPost\"" in rContent)
        self.assertTrue("<input type=\"text\" name=\"tagsPost\"" in rContent)

class edit(TestCase):
    def test_basicPage(self):
        todoDict = {}
        todoDict['title']="testTitle"
        todoDict['description']="testDescription"
        todoDict['creation_date']="2022-01-01T12:00"
        todoDict['due_date']="2022-01-01T12:00"
        todoDict['status']="testStatus"
        todoDict['tags']="testTag0 testTag1"
        todo.objects.create_todo(todoDict)


        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 404)
        response = client.get(reverse('djangoTask:detail', kwargs={'todo_id': 1}))
        self.assertEqual(response.status_code, 200)
        rContent = response.content.decode("utf-8")
        self.assertIs("<h1>"+todoDict['title']+"</h1>" in rContent, True)
        self.assertIs("</table>" in rContent, True)
        self.assertIs("<td>Title</td>" in rContent, True)
        self.assertIs("<td>Description</td>" in rContent, True)
        self.assertIs("<td>Creation Date</td>" in rContent, True)
        self.assertIs("<td>Due Date</td>" in rContent, True)
        self.assertIs("<td>Status</td>" in rContent, True)
        self.assertIs("<td>Tags</td>" in rContent, True)

        self.assertTrue("<input type=\"text\" name=\"title\" id=\"title\" value=\""+todoDict['title']+"\">" in rContent)
        self.assertTrue("<input type=\"text\" name=\"descriptionPost\" value=\""+todoDict['description']+"\">" in rContent)
        self.assertTrue("<input type=\"datetime-local\" name=\"creationDatePost\" value=\""+todoDict['creation_date']+"\">" in rContent)
        self.assertTrue("<input type=\"datetime-local\" name=\"dueDatePost\" value=\""+todoDict['due_date']+"\">" in rContent)
        self.assertTrue("<input type=\"text\" name=\"statusPost\" value=\""+todoDict['status']+"\">" in rContent)
        self.assertTrue("<input type=\"text\" name=\"tagsPost\" value=\""+todoDict['tags']+"\">" in rContent)


    # # todo
    #     - posts
    #         - edit
    #         - create
    #     - [x] new view
    #     - [x] detail view
    #     - about view
    #     - blank view
