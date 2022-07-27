from django.db import models
import json
from django.utils import timezone
from datetime import datetime

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
                output += todo_t.setCreationDateFromString(context['creation_date'])
            except:
                output += todo_t.setCreationDate(datetime.utcnow())

            try:
                output += todo_t.setDueDateFromString(context['due_date'])
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
        # print("output = ", output)
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
        output = "["
        todoList =todo.objects.all()
        for i in todo.objects.all():
            output += json.dumps(i.getAsDict())
            output +=","
        if output[-1]==",":
            output=output[:-1]
        output+="]"
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
    def setCreationDate(self,i): #from datetime param
        output = ""
        try:
            self.creation_date = i
            self.save()
        except:
            self.creation_date = None
            output = "could not set creation date with input " + i
        return output
    def setCreationDateFromString(self,i):
        output = ""
        try:
            dateTime_t = datetime.fromisoformat(i)
            if not(dateTime_t.tzinfo and (dateTime_t.tzinfo.utcoffset(dateTime_t)!=None)):
                print(" dateTime_t doesn't look aware")
                tz_t = "+00:00" #TODO: refine timezones for local lookup
                dateTime_t = datetime.fromisoformat(i+tz_t)
                print("dateTime_t now = ", dateTime_t.isoformat())
            output =  self.setCreationDate(dateTime_t)
        except:
            output += "setCreationDateFromString() failed"
        return output
    def setDueDate(self,i):
        output = ""
        try:
            self.due_date = i
            self.save()
        except:
            self.due_date = None
            output = "could not set due date with input " + i
        return output
    def setDueDateFromString(self,i):
        output = ""
        try:
            dateTime_t = datetime.fromisoformat(i)
            print("dateTime_t = ", dateTime_t.isoformat())
            if not(dateTime_t.tzinfo and (dateTime_t.tzinfo.utcoffset(dateTime_t)!=None)):
                print(" dateTime_t doesn't look aware")
                tz_t = "+00:00" #TODO: refine timezones for local lookup
                dateTime_t = datetime.fromisoformat(i+tz_t)
                print("dateTime_t now = ", dateTime_t.isoformat())
            output = self.setDueDate(dateTime_t)
        except:
            output += "setDueDateFromString() failed"
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

    def getAsDict(self):
        output = {}
        output['title']=self.title
        output['description']=self.description
        try: # dates may be null
            output['creation_date']=self.creation_date.isoformat()
        except:
            pass
        try:
            output['due_date']=self.due_date.isoformat()
        except:
            pass
        output['status']=self.status
        output['tags']=self.tags
        return output
