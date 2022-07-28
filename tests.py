from django.test import TestCase
from django.test import Client
from django.test.utils import setup_test_environment
from django.urls import reverse
from .models import todo, todoManager, jsonExample, dictToString, jsonExampleImportString
from datetime import datetime

def createTodoFromExample():
        todoDict = {}
        todoDict['title']=jsonExample['title']
        todoDict['description']=jsonExample['description']
        todoDict['creation_date']=jsonExample['creation_date']
        todoDict['due_date']=jsonExample['due_date']
        todoDict['status']=jsonExample['status']
        todoDict['tags']=jsonExample['tags']
        todo.objects.create_todo(todoDict)

class index(TestCase):
    def test_basicPage(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 404)
        response = client.get(reverse('djangoTask:index'))
        self.assertEqual(response.status_code, 200)
        rContent = response.content.decode("utf-8")
        self.assertTrue("<title>Todo Index</title>" in rContent)
        self.assertTrue("<p>No todos are available.</p>" in rContent)

        # no table if no todos exist
        self.assertFalse("</table>" in rContent)


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
        self.assertTrue("<h1>NEW</h1>" in rContent)
        self.assertTrue("</table>" in rContent)
        self.assertTrue("<td>Title</td>" in rContent)
        self.assertTrue("<td>Description</td>" in rContent)
        self.assertTrue("<td>Creation Date</td>" in rContent)
        self.assertTrue("<td>Due Date</td>" in rContent)
        self.assertTrue("<td>Status</td>" in rContent)
        self.assertTrue("<td>Tags</td>" in rContent)

        self.assertTrue("<input type=\"text\" name=\"title\" id=\"title\" value=\"NEW\">" in rContent)
        self.assertTrue("<input type=\"text\" name=\"description\"" in rContent)
        self.assertTrue("<input type=\"datetime-local\" name=\"creationDate\"" in rContent)
        self.assertTrue("<input type=\"datetime-local\" name=\"dueDate\"" in rContent)
        self.assertTrue("<input type=\"datetime-local\" name=\"dueDate\"" in rContent)
        self.assertTrue("<input type=\"text\" name=\"status\"" in rContent)
        self.assertTrue("<input type=\"text\" name=\"tags\"" in rContent)

class edit(TestCase):
    def test_basicPage(self):
        createTodoFromExample()
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 404)
        response = client.get(reverse('djangoTask:detail', kwargs={'todo_id': 1}))
        self.assertEqual(response.status_code, 200)
        rContent = response.content.decode("utf-8")
        self.assertTrue("<h1>"+jsonExample['title']+"</h1>" in rContent)
        self.assertTrue("</table>" in rContent)
        self.assertTrue("<td>Title</td>" in rContent)
        self.assertTrue("<td>Description</td>" in rContent)
        self.assertTrue("<td>Creation Date</td>" in rContent)
        self.assertTrue("<td>Due Date</td>" in rContent)
        self.assertTrue("<td>Status</td>" in rContent)
        self.assertTrue("<td>Tags</td>" in rContent)

        self.assertTrue("<input type=\"text\" name=\"title\" id=\"title\" value=\""+jsonExample['title']+"\">" in rContent)
        self.assertTrue("<input type=\"text\" name=\"description\" value=\""+jsonExample['description']+"\">" in rContent)

        # datetime-local needs specialized formatting that devieates from ISO standard
        self.assertTrue("<input type=\"datetime-local\" name=\"creationDate\" value=\""+jsonExample['creation_date'][:16]+"\">" in rContent)
        self.assertTrue("<input type=\"datetime-local\" name=\"dueDate\" value=\""+jsonExample['due_date'][:16]+"\">" in rContent)

        self.assertTrue("<input type=\"text\" name=\"status\" value=\""+jsonExample['status']+"\">" in rContent)
        self.assertTrue("<input type=\"text\" name=\"tags\" value=\""+jsonExample['tags']+"\">" in rContent)

class about(TestCase):
    def test_basicPage(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 404)
        response = client.get(reverse('djangoTask:about'))
        self.assertEqual(response.status_code, 200)
        rContent = response.content.decode("utf-8")
        self.assertTrue("<h1>About</h1>" in rContent)
        self.assertTrue("<i>djangoTask</i>" in rContent)

class base(TestCase):
    def test_basicPage(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 404)
        response = client.get(reverse('djangoTask:base'))
        self.assertEqual(response.status_code, 200)
        rContent = response.content.decode("utf-8")
        self.assertFalse("<h1>" in rContent)
        self.assertTrue("<p>Base class template that is extended for other templates</p>" in rContent)

class importPage(TestCase):
    def test_basicPage(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 404)
        response = client.get(reverse('djangoTask:import'))
        self.assertEqual(response.status_code, 200)
        rContent = response.content.decode("utf-8")
        self.assertTrue("<p>Input data in text box or by upload (example below)</p>" in rContent)
        self.assertTrue("<textarea name=\"inData\" id=\"inData\"" in rContent)
        self.assertTrue(dictToString(jsonExample).replace("\"", "&quot;") in rContent)
        self.assertTrue("<input type=\"submit\" value=\"save\">" in rContent)

class exportPage(TestCase):
    def test_basicPage(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 404)
        response = client.get(reverse('djangoTask:export'))
        self.assertEqual(response.status_code, 200)
        rContent = response.content.decode("utf-8")
        #empty until a todo has been created

        self.assertTrue("<p>[]</p>" in rContent)

        createTodoFromExample()
        response = client.get(reverse('djangoTask:export'))
        self.assertEqual(response.status_code, 200)
        rContent = response.content.decode("utf-8")

        # example used, but djanog somehow modifies it to a functionally identical version
        # create a 'revised' (_r) version and look for that
        jsonExampleImportString_r = jsonExampleImportString.replace("\"","&quot;")
        jsonExampleImportString_r = jsonExampleImportString_r.replace("&quot;:","&quot;: ")
        jsonExampleImportString_r = jsonExampleImportString_r.replace("&quot;,","&quot;, ")
        self.assertTrue("<p>"+jsonExampleImportString_r+"</p>" in rContent)


class newPost(TestCase):
    def test_newPost(self):
        c = Client()
        postContent = jsonExample
        postContent['creationDate']= jsonExample['creation_date'][:16]
        postContent['dueDate']= jsonExample['due_date'][:16]
        response= c.post(reverse('djangoTask:createPost'), jsonExample, follow=True)

        # Confirm data in table is correct
        self.assertEqual(200, response.status_code)
        rContent = response.content.decode("utf-8")
        self.assertTrue(jsonExample['title'] in rContent)
        self.assertTrue(jsonExample['status'] in rContent)
        self.assertTrue(jsonExample['dueDate'][:10] in rContent)

        # Confirm whole object is correct
        todo_t = todo.objects.all()[0]
        self.assertEqual(jsonExample['title'], todo_t.title)
        self.assertEqual(jsonExample['description'], todo_t.description)
        self.assertEqual(jsonExample['due_date'], todo_t.due_date.isoformat())
        self.assertEqual(jsonExample['creation_date'], todo_t.creation_date.isoformat())
        self.assertEqual(jsonExample['status'], todo_t.status)
        self.assertEqual(jsonExample['tags'], todo_t.tags)

class editPost(TestCase):
    def test_editPost(self):
        createTodoFromExample()

        editDict = {}
        editDict['title'] = "changed title"
        editDict['description'] = "changed description"
        editDict['dueDate'] = "2050-01-01T00:00:00" #will not receive TZ from edit page
        editDict['creationDate'] = "2050-01-01T12:00:00"
        editDict['status'] = "newStatus"
        editDict['tags'] = "newTag1 newTag2"


        c = Client()
        postContent = jsonExample
        response= c.post(reverse('djangoTask:editPost', kwargs={'todo_id': 1}), editDict, follow=True)

        # Confirm data in table is correct
        self.assertEqual(200, response.status_code)
        rContent = response.content.decode("utf-8")
        self.assertTrue(editDict['title'] in rContent)
        self.assertTrue(editDict['status'] in rContent)
        self.assertTrue(editDict['dueDate'][:10] in rContent)

        # Confirm whole object is correct
        todo_t = todo.objects.all()[0]
        self.assertEqual(editDict['title'], todo_t.title)
        self.assertEqual(editDict['description'], todo_t.description)
        self.assertEqual(editDict['dueDate']+"+00:00", todo_t.due_date.isoformat())
        self.assertEqual(editDict['creationDate']+"+00:00", todo_t.creation_date.isoformat())
        self.assertEqual(editDict['status'], todo_t.status)
        self.assertEqual(editDict['tags'], todo_t.tags)


class importPost(TestCase):
    def test_singleImport(self):
        self.assertEqual(0,len(todo.objects.all()))
        postDict = {}
        postDict['inData']=jsonExampleImportString
        c = Client()
        response= c.post(reverse('djangoTask:import'), postDict, follow=True)

        self.assertEqual(1,len(todo.objects.all()))
        # Confirm whole object is correct
        todo_t = todo.objects.all()[0]
        self.assertEqual(jsonExample['title'], todo_t.title)
        self.assertEqual(jsonExample['description'], todo_t.description)
        self.assertEqual(jsonExample['due_date'], todo_t.due_date.isoformat())
        self.assertEqual(jsonExample['creation_date'], todo_t.creation_date.isoformat())
        self.assertEqual(jsonExample['status'], todo_t.status)
        self.assertEqual(jsonExample['tags'], todo_t.tags)

    def test_multiImport(self):
        # create ten identical items
        items=10
        self.assertEqual(0,len(todo.objects.all()))
        postDict = {}
        extendedString = "["
        examplePart = jsonExampleImportString[1:-1]
        for i in range(items):
            extendedString+=examplePart+","
        extendedString = extendedString[:-1]
        extendedString+="]"
        postDict['inData']=extendedString
        c = Client()
        response= c.post(reverse('djangoTask:import'), postDict, follow=True)

        self.assertEqual(items,len(todo.objects.all()))
        # Confirm whole object is correct

        for i in range(items):
            todo_t = todo.objects.all()[i]
            self.assertEqual(jsonExample['title'], todo_t.title)
            self.assertEqual(jsonExample['description'], todo_t.description)
            self.assertEqual(jsonExample['due_date'], todo_t.due_date.isoformat())
            self.assertEqual(jsonExample['creation_date'], todo_t.creation_date.isoformat())
            self.assertEqual(jsonExample['status'], todo_t.status)
            self.assertEqual(jsonExample['tags'], todo_t.tags)


    # # todo
    #     - posts
    #       - [x] create
    #       - [x] edit
    #       - [x] import
    #       - [ ] delete
    #     -Views
    #       - [x] index
    #       - [x] new view
    #       - [x] detail view
    #       - [x] about view
    #       - [x] blank view
    #       - [x] import
    #       - [x] export
