from django.test import TestCase
from django.test import Client
from django.test.utils import setup_test_environment
from django.urls import reverse
from .models import todo, todoManager, jsonExample, dictToString, jsonExampleImportString
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, User
import json
from rest_framework import status as statusRF

def createTodoFromExample():
    todoDict = {}
    todoDict['title']=jsonExample['title']
    todoDict['description']=jsonExample['description']
    todoDict['creation_date']=jsonExample['creation_date']
    todoDict['due_date']=jsonExample['due_date']
    todoDict['status']=jsonExample['status']
    todoDict['tags']=jsonExample['tags']
    todoDict['owner']=jsonExample['owner']
    todo.objects.create_todo(todoDict)

class index(TestCase):
    def test_404(self):
        client = Client()
        response = client.get("todo/")
        self.assertEqual(response.status_code, 404)

    def test_basicPage(self):
        client = Client()
        response = client.get(reverse('djangoTask:index'))
        self.assertEqual(response.status_code, 200)
        rContent = response.content.decode("utf-8")
        self.assertTrue("<title>Todo Index</title>" in rContent)
        self.assertTrue("<p>No todos are available.</p>" in rContent)

        # no table if no todos exist
        self.assertFalse("</table>" in rContent)

    def test_todoInIndex(self):
        superuser_t = User.objects.create_user("superUser", password="abcd")
        createTodoFromExample()
        client = Client()
        response = client.get(reverse('djangoTask:index'))
        rContent = response.content.decode("utf-8")
        self.assertTrue("</table>" in rContent)

        self.assertEqual(200, response.status_code)
        self.assertTrue(jsonExample['title'] in rContent)
        self.assertTrue(jsonExample['status'] in rContent)
        self.assertTrue(jsonExample['due_date'][:10] in rContent)

    def test_multipletodosInIndex(self):
        """ create 99 todos and check that they're all in the table """
        todoList = []
        todoMax = 99
        range_t = range(0,todoMax)
        for i in range_t:
            dict_t = {}
            title_t = "testTitle"+str(i)
            dict_t['title']=title_t
            todo_t = todo.objects.create_todo(dict_t)
            lastIdx = len(todo.objects.all()) - 1#last index
            todo_t = todo.objects.all()[lastIdx]
            todoList.append({'title':todo_t.title,'id':todo_t.id})
        client = Client()
        url_t = reverse('djangoTask:index')
        response = client.get(url_t)
        rContent = response.content.decode("utf-8")
        self.assertTrue("</table>" in rContent)
        for i in todoList:
            testString = "<a href=\"/todo/"+str(i['id'])+"/\">"+i['title']+"</a>"
            if testString not in rContent:
                logging.error("missing :"+testString)
            self.assertTrue(testString in rContent)

class new(TestCase):
    def test_basicPage(self):
        client = Client()
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
        superuser_t = User.objects.create_user("superUser", password="abcd")
        createTodoFromExample()
        client = Client()
        id_t=todo.objects.all()[0].id # get id from the only existing todo
        url_t = reverse('djangoTask:detail', kwargs={'todo_id': id_t})
        response = client.get(url_t)
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
        response = client.get(reverse('djangoTask:about'))
        self.assertEqual(response.status_code, 200)
        rContent = response.content.decode("utf-8")
        self.assertTrue("<h1>About</h1>" in rContent)
        self.assertTrue("<i>djangoTask</i>" in rContent)

class base(TestCase):
    def test_basicPage(self):
        client = Client()
        response = client.get(reverse('djangoTask:base'))
        self.assertEqual(response.status_code, 200)
        rContent = response.content.decode("utf-8")
        self.assertFalse("<h1>" in rContent)
        self.assertTrue("<p>Base class template that is extended for other templates</p>" in rContent)

class importPage(TestCase):
    def test_basicPage(self):
        client = Client()
        response = client.get(reverse('djangoTask:import'))
        self.assertEqual(response.status_code, 200)
        rContent = response.content.decode("utf-8")
        self.assertTrue("<p>Input data in text box or by upload (example below)</p>" in rContent)
        self.assertTrue("<textarea name=\"inData\" id=\"inData\"" in rContent)
        self.assertTrue(dictToString(jsonExample).replace("\"", "&quot;") in rContent)
        self.assertTrue("<input type=\"submit\" value=\"save\">" in rContent)

class exportPage(TestCase):
    def test_basicPage(self):
        superuser_t = User.objects.create_user("superUser", password="abcd")
        client = Client()
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
        superuser_t = User.objects.create_user("superUser", password="abcd")
        user_t = User.objects.create_user("testUser", password="abcd")
        content_type = ContentType.objects.get_for_model(todo, for_concrete_model=False)
        permission = Permission.objects.get(codename='add_todo',content_type=content_type,)
        user_t.user_permissions.add(permission)
        c = Client()
        c.login(username="testUser", password="abcd")

        postContent = jsonExample
        postContent['creationDate']= jsonExample['creation_date'][:16]
        postContent['dueDate']= jsonExample['due_date'][:16]
        response= c.post(reverse('djangoTask:createPost'), postContent, follow=True)

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
        self.assertEqual(jsonExample['owner'], todo_t.owner.username)

class editPost(TestCase):
    def test_editPost(self):
        superuser_t = User.objects.create_user("superUser", password="abcd")
        user_t = User.objects.create_user("testUser", password="abcd")
        content_type = ContentType.objects.get_for_model(todo, for_concrete_model=False)
        permission = Permission.objects.get(codename='add_todo',content_type=content_type,)
        user_t.user_permissions.add(permission)
        permission = Permission.objects.get(codename='change_todo',content_type=content_type,)
        user_t.user_permissions.add(permission)
        createTodoFromExample()

        editDict = {}
        editDict['title'] = "changed title"
        editDict['description'] = "changed description"
        editDict['dueDate'] = "2050-01-01T00:00:00" #will not receive TZ from edit page
        editDict['creationDate'] = "2050-01-01T12:00:00"
        editDict['status'] = "newStatus"
        editDict['tags'] = "newTag1 newTag2"
        editDict['owner'] = "testUser"


        c = Client()
        c.login(username="testUser", password="abcd")
        postContent = jsonExample
        id_t = todo.objects.all()[0].id
        response= c.post(reverse('djangoTask:editPost', kwargs={'todo_id': id_t}), editDict, follow=True)

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
        self.assertEqual(editDict['owner'], todo_t.owner.username)


class importPost(TestCase):
    def test_singleImport(self):
        self.assertEqual(0,len(todo.objects.all()))
        superuser_t = User.objects.create_user("superUser", password="abcd")
        user_t = User.objects.create_user("testUser", password="abcd")
        content_type = ContentType.objects.get_for_model(todo, for_concrete_model=False)
        permission = Permission.objects.get(codename='add_todo',content_type=content_type,)
        user_t.user_permissions.add(permission)


        postDict = {}
        postDict['inData']=jsonExampleImportString
        c = Client()
        c.login(username="testUser", password="abcd")
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
        superuser_t = User.objects.create_user("superUser", password="abcd")
        user_t = User.objects.create_user("testUser", password="abcd")
        content_type = ContentType.objects.get_for_model(todo, for_concrete_model=False)
        permission = Permission.objects.get(codename='add_todo',content_type=content_type,)
        user_t.user_permissions.add(permission)
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
        c.login(username="testUser", password="abcd")
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

class deletePost(TestCase):
    def test_deleteBlank(self):
        c = Client()
        postDict = {}
        postDict['todo_id'] = 1
        response= c.post(reverse('djangoTask:delete'), postDict, follow=True)
        self.assertEqual(response.status_code, 200)
        rContent = response.content.decode("utf-8")

        #should have no todos visible at Index
        self.assertTrue("<title>Todo Index</title>" in rContent)
        self.assertTrue("<p>No todos are available.</p>" in rContent)

    def test_delete(self):
        superuser_t = User.objects.create_user("superUser", password="abcd")
        user_t = User.objects.create_user("testUser", password="abcd")
        content_type = ContentType.objects.get_for_model(todo, for_concrete_model=False)
        permission = Permission.objects.get(codename='delete_todo',content_type=content_type,)
        user_t.user_permissions.add(permission)

        #add a todo
        createTodoFromExample()

        # check that the todo shows up in the index
        c = Client()
        c.login(username="testUser", password="abcd")
        response = c.get(reverse('djangoTask:index'))
        rContent = response.content.decode("utf-8")
        self.assertTrue("</table>" in rContent)
        self.assertEqual(200, response.status_code)
        self.assertTrue(jsonExample['title'] in rContent)
        self.assertTrue(jsonExample['status'] in rContent)
        self.assertTrue(jsonExample['due_date'][:10] in rContent)

        #delete the todo
        postDict = {}
        postDict['todo_id'] = todo.objects.all()[0].id
        response= c.post(reverse('djangoTask:delete'), postDict, follow=True)
        self.assertEqual(response.status_code, 200)
        rContent = response.content.decode("utf-8")

        #confirm  no todos visible at Index
        self.assertTrue("<title>Todo Index</title>" in rContent)
        self.assertTrue("<p>No todos are available.</p>" in rContent)

class api(TestCase):
    def test_getRoot(self):
        superuser_t = User.objects.create_user("superUser", password="abcd")
        createTodoFromExample()
        c = Client()
        response = c.get(reverse('djangoTask:api'))
        self.assertEqual(response.status_code, 200)
        rContent = response.content.decode("utf-8")
        d = json.loads(rContent)
        for i in d:
            self.assertEqual(jsonExample['title'],i['title'])
            self.assertEqual(jsonExample['description'],i['description'])
            # TODO - add these checks back in once timezone handling is corrected
            # self.assertEqual(jsonExample['creation_date'],i['creation_date'])
            # self.assertEqual(jsonExample['due_date'],i['due_date'])
            self.assertEqual(jsonExample['status'],i['status'])
            self.assertEqual(jsonExample['tags'],i['tags'])
    def test_getItems(self):
        superuser_t = User.objects.create_user("superUser", password="abcd")
        createTodoFromExample()
        id_t = todo.objects.all()[0].id
        c = Client()
        response = c.get(reverse('djangoTask:apiIdx', kwargs={'pk': id_t}))
        self.assertEqual(response.status_code, 200)
        rContent = response.content.decode("utf-8")
        d = json.loads(rContent)
        self.assertEqual(jsonExample['title'],d['title'])
        self.assertEqual(jsonExample['description'],d['description'])
        self.assertEqual(jsonExample['status'],d['status'])
        self.assertEqual(jsonExample['tags'],d['tags'])
        # TODO - add these checks back in once timezone handling is corrected
        # self.assertEqual(jsonExample['creation_date'],d['creation_date'])
        # self.assertEqual(jsonExample['due_date'],d['due_date'])

    def test_post(self):
        superuser_t = User.objects.create_user("superUser", password="abcd")
        user_t = User.objects.create_user("testUser", password="abcd")
        content_type = ContentType.objects.get_for_model(todo, for_concrete_model=False)
        permission = Permission.objects.get(codename='add_todo',content_type=content_type,)
        user_t.user_permissions.add(permission)

        c = Client()
        c.login(username="testUser", password="abcd")
        editDict = {}
        editDict['title'] = "changed title"
        editDict['creation_date'] = "2050-01-01T12:00:00+0000"
        editDict['due_date'] = "2050-01-01T00:00:00+0000" #will not receive
        response = c.post(reverse('djangoTask:api'), jsonExample, follow=True)
        self.assertEqual(statusRF.HTTP_201_CREATED, response.status_code)
        todo_t = todo.objects.all()[0]
        self.assertEqual(jsonExample['title'], todo_t.title)
        self.assertEqual(jsonExample['description'], todo_t.description)
        self.assertEqual(jsonExample['due_date'], todo_t.due_date.isoformat())
        self.assertEqual(jsonExample['creation_date'], todo_t.creation_date.isoformat())
        self.assertEqual(jsonExample['status'], todo_t.status)
        self.assertEqual(jsonExample['tags'], todo_t.tags)

class apiIdx(TestCase):
    def test_get(self):
        superuser_t = User.objects.create_user("superUser", password="abcd")
        createTodoFromExample()
        c = Client()
        id_t = todo.objects.all()[0].id
        response = c.get(reverse('djangoTask:apiIdx', kwargs={'pk': id_t}))
        self.assertEqual(response.status_code, 200)
        d = json.loads(response.content.decode("utf-8"))
        self.assertEqual(jsonExample['title'], d['title'])
        self.assertEqual(jsonExample['description'], d['description'])
        # TODO - add these checks back in once timezone handling is corrected
        # self.assertEqual(jsonExample['due_date'], d['due_date'])
        # self.assertEqual(jsonExample['creation_date'], d['creation_date'])
        self.assertEqual(jsonExample['status'], d['status'])
        self.assertEqual(jsonExample['tags'], d['tags'])

        # TODO - add this .api (.html) request once bootstrap loading error is fixed
        # url_api = reverse('djangoTask:apiIdx', kwargs={'pk': id_t})
        # url_api = url_api[0:-1]+".api"
        # print("url_api = ",url_api)
        # response = c.get(url_api)
        # self.assertEqual(response.status_code, 200)
        # rContent = response.content.decode("utf-8")
        # print(rContent)
        # self.assertTrue("<html>" in rContent)



    def test_put(self):
        superuser_t = User.objects.create_user("superUser", password="abcd")
        user_t = User.objects.create_user("testUser", password="abcd")
        content_type = ContentType.objects.get_for_model(todo, for_concrete_model=False)
        permission = Permission.objects.get(codename='add_todo',content_type=content_type,)
        user_t.user_permissions.add(permission)
        editDict = {}
        editDict['title'] = "changed title"
        editDict['creation_date'] = "2020-01-01T01:01:00+0000"
        editDict['due_date'] = "2020-01-01T01:01:00+0000"
        editDict['description'] = "new description"
        editDict['status'] = "new status"
        editDict['tags'] = "new tags"
        c = Client()
        c.login(username="testUser", password="abcd")

        # Invalid ID
        url_t = reverse('djangoTask:apiIdx', kwargs={'pk': 0})
        # setting the content_type was necessary and made me insane for >20min
        response = c.put(url_t,data=editDict,content_type='application/json', follow=True)
        self.assertEqual(404, response.status_code)

        createTodoFromExample()
        id_t = todo.objects.all()[0].id
        url_t = reverse('djangoTask:apiIdx', kwargs={'pk': id_t})

        # unsuccessful Put with garbage date:
        editDict['creation_date'] = "NotARealDate"
        response = c.put(url_t,data=editDict,content_type='application/json', follow=True)
        self.assertEqual(400, response.status_code)

        # successful Put
        editDict['creation_date'] = "2020-01-01T01:01:00+0000"
        response = c.put(url_t,data=editDict,content_type='application/json', follow=True)
        self.assertEqual(200, response.status_code)
        d = json.loads(response.content.decode("utf-8"))
        self.assertEqual(editDict['title'], d['title'])
        self.assertEqual(editDict['description'], d['description'])
        self.assertEqual(editDict['creation_date'], d['creation_date'])
        self.assertEqual(editDict['due_date'], d['due_date'])
        self.assertEqual(editDict['status'], d['status'])
        self.assertEqual(editDict['tags'], d['tags'])

    def test_delete(self):
        superuser_t = User.objects.create_user("superUser", password="abcd")
        user_t = User.objects.create_user("testUser", password="abcd")
        content_type = ContentType.objects.get_for_model(todo, for_concrete_model=False)
        permission = Permission.objects.get(codename='delete_todo',content_type=content_type,)
        user_t.user_permissions.add(permission)
        createTodoFromExample()
        c = Client()
        c.login(username="testUser", password="abcd")
        id_t = todo.objects.all()[0].id
        url_t = reverse('djangoTask:apiIdx', kwargs={'pk': id_t})
        response = c.delete(url_t, follow=True)
        self.assertEqual(statusRF.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(0, len(todo.objects.all()))
