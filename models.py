from django.db import models
import json
from django.utils import timezone

def dictToString(context):
    output = ""
    try:
        output += "{"
        for x,y in context.items():
            output+="\""+str(x)+"\":"+"\""+str(y)+"\","
        if output[-1]==",":
            output=output[:-1]
        output +="}"
    except:
        output+="dictToString Failed!"
        print(context)
    return output

class todoManager(models.Manager):
    def create_todo(self, context):
        output = ""
        try:
            # this will break try before creating a new todo
            title_t = context['title']

            todo_t = self.create()
            output += todo_t.setTitle(title_t)
            print("create_todo() succeeded!")

            try:
                output += todo_t.setDescription(context['description'])
            except:
                output += todo_t.setDescription("")

            try:
                output += todo_t.setCreationDate(context['creation_date'])
            except:
                output += todo_t.setCreationDate(timezone.now().strftime('%Y-%m-%dT%H:%M %z'))

            try:
                output += todo_t.setDueDate(context['due_date'])
            except:
                print("no due-date specified.  Will remain Null")

            try:
                output += todo_t.setStatus(context['status'])
            except:
                output += todo_t.setStatus("open")

            try:
                output += todo_t.setTags(context['tags'])
            except:
                output += todo_t.setTags("")

        except:
            output+= "could not create from " + dictToString(context)
            print("create_todo() failed.")

        print("output = ", output)
        return output
    def createFromJson(self, inText):
        output = ""
        try:
            print(inText)
            d = json.loads(inText)
            print(d)
            objectsOriginal=len(self.all())
            if len(d) > 0:
                for i in d:
                    print(i)
                    output += self.create_todo(i)
            else:
                print("no valid json objects found")
            objectsCreated= len(self.all())-objectsOriginal
            print("todo objects:", objectsCreated )

            output += " Created "+str(objectsCreated)+" todos"
        except:
            output+="JSON input could not be parsed."
        return output
    def getJson(self):
        ### creates json export of all todos
        output = "{"
        # print(self.all())
        # output +=
        todoList =todo.objects.all()
        # todo0=todoList[0]
        # print(todo0.getAsDict())
        for i in todo.objects.all():
            output += json.dumps(i.getAsDict())

        # if output[-1] == ",":
        #     output = output[:-1]
        output+="}"
        return output

class todo(models.Model):
    title=models.CharField(max_length=200)
    description=models.CharField(max_length=2000, blank=True, null=True)
    creation_date=models.DateTimeField('date created', blank=True, null=True)
    due_date=models.DateTimeField('date due', blank=True, null=True)
    status=models.CharField(max_length=100, blank=True, null=True)
    tags=models.CharField(max_length=200, blank=True, null=True)
    objects = todoManager()

    def __str__(self):
        return self.title

    # set functions are good in principal and will be helpful for handling logs later
    def setTitle(self,i):
        # self.title=i
        output = ""
        try:
            self.title = i
            self.save()
        except:
            output = "could not set title with input " + i
        return output
    def setDescription(self,i):
        output = ""
        try:
            self.description = i
            self.save()
        except:
            output = "could not set description with input " + i
        return output
    def setCreationDate(self,i):
        output = ""
        try:
            self.creation_date = i
            self.save()
        except:
            output = "could not set creation date with input " + i
        return output
    def setDueDate(self,i):
        output = ""
        try:
            self.due_date = i
            self.save()
        except:
            output = "could not set due date with input " + i
        return output
    def setStatus(self,i):
        output = ""
        try:
            self.status = i
            self.save()
        except:
            output = "could not set status with input " + i
        return output
    def setTags(self,i):
        output = ""
        try:
            self.tags = i
            self.save()
        except:
            output = "could not set tags with input " + i
        return output


    def convertToDateTimeFormat(self,i, option = ""):
        output = ""
        try:
            if option == "dateOnly":
                output = i.strftime('%Y-%m-%d')
            else:
                output = i.strftime('%Y-%m-%dT%H:%M %z')
        except:
            output+= ""
        return output

    def getCreationDate(self):
        return self.convertToDateTimeFormat(self.creation_date, "dateOnly")

    def getCreationDateTime(self):
        return self.convertToDateTimeFormat(self.creation_date)

    def getDueDate(self):
        output=""
        try:
            output = self.convertToDateTimeFormat(self.due_date, "dateOnly")
        except:
            output += "getDueDate() failed"
            # print("getDueDate() failed")
        return output

    def getDueDateTime(self):
        return self.convertToDateTimeFormat(self.due_date)

    def getAsDict(self):
        output = {}
        output['title']=self.title
        output['description']=self.description
        output['creation_date']=self.getCreationDateTime()
        output['due_date']=self.getDueDateTime()
        output['status']=self.status
        output['tags']=self.tags
        return output
