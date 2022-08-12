from django.db import models
import json
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User

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

jsonExample = {}
jsonExample['title'] = "Sample Title"
jsonExample['description'] = "sample description"
jsonExample['creation_date'] = "2022-07-27T17:00:00+00:00"
jsonExample['due_date'] = "2022-08-07T17:00:00+00:00"
jsonExample['status'] = "pending"
jsonExample['tags'] = "tf69"
jsonExample['owner'] = "superUser"
jsonExampleImportString="["+dictToString(jsonExample)+"]"
# "[{\"title\": \"Sample Title\", \"description\": \"sample description\", \"creation_date\": \"2022-07-27T17:00:00+00:00\", \"due_date\": \"2022-07-27T17:00:00+00:00\", \"status\": \"pending\", \"tags\": \"TF69\"}]"

class todoManager(models.Manager):
    def create_todo(self, context):
        output = ""
        try:
            # this will break try before creating a new todo
            title_t = context['title']

            todo_t = self.create()
            output += todo_t.setTitle(title_t)

            if 'owner' in context:
                output += todo_t.setOwner(context['owner'])

            if 'description' in context:
                output += todo_t.setDescription(context['description'])


            if 'creation_date' in context:
                output += todo_t.setCreationDateFromString(context['creation_date'])
            # else:
            #     output += todo_t.setCreationDate(datetime.now(timezone.utc))

            if 'due_date' in context:
                output += todo_t.setDueDateFromString(context['due_date'])

            if 'status' in context:
                output += todo_t.setStatus(context['status'])

            if 'tags' in context:
                output += todo_t.setTags(context['tags'])

        except:
            output+= "could not create from " + dictToString(context)
            output += "create_todo() failed."
            print(output)
        # print("output = ", output)
        return output
    def createFromJson(self, inText):
        output = ""
        try:
            # print(inText)
            d = json.loads(inText)
            # print(d)
            objectsOriginal=len(self.all())
            if len(d) > 0:
                for i in d:
                    # print(i)
                    output += self.create_todo(i)
            else:
                print("no valid json objects found")
            objectsCreated= len(self.all())-objectsOriginal
            # print("todo objects:", objectsCreated )

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
    creation_date=models.DateTimeField('date created', blank=True, null=True, default=timezone.now)
    due_date=models.DateTimeField('date due', blank=True, null=True)
    status=models.CharField(max_length=100, blank=True, null=True, default="open")
    tags=models.CharField(max_length=200, blank=True, null=True)
    objects = todoManager()
    owner = models.ForeignKey('auth.User', related_name='todos', on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering=['creation_date']

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
    def setOwner(self,i):
        output = ""
        if i == "":
            i = None
            print("set i to \"None\".")
        try:
            user_t = User.objects.get(username=i)
            self.owner = user_t
            print("setting self.owner to "+str(self.owner))
            self.save()
        except:
            output = "could not set owner to " + i
            print(output)
        print("self.owner = "+str(self.owner))
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
                # print(" dateTime_t doesn't look aware")
                tz_t = "+00:00" #TODO: refine timezones for local lookup
                dateTime_t = datetime.fromisoformat(i+tz_t)
                # print("dateTime_t now = ", dateTime_t.isoformat())
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
            # print("dateTime_t = ", dateTime_t.isoformat())
            if not(dateTime_t.tzinfo and (dateTime_t.tzinfo.utcoffset(dateTime_t)!=None)):
                # print(" dateTime_t doesn't look aware")
                tz_t = "+00:00" #TODO: refine timezones for local lookup
                dateTime_t = datetime.fromisoformat(i+tz_t)
                # print("dateTime_t now = ", dateTime_t.isoformat())
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
        output['owner']=str(self.owner)
        return output
