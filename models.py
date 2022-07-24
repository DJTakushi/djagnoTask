from django.db import models

class todo(models.Model):
    title=models.CharField(max_length=200)
    description=models.CharField(max_length=2000)
    creation_date=models.DateTimeField('date created')
    due_date=models.DateTimeField('date due')
    status=models.CharField(max_length=100)
    tags=models.CharField(max_length=200)

    def __str__(self):
        return self.title

    def convertToDateTimeFormat(self,i, option = ""):
        output = ""
        if option == "dateOnly":
            output = i.strftime('%Y-%m-%d')
        else:
            output = i.strftime('%Y-%m-%dT%H:%M')
        return output

    def getCreationDate(self):
        return self.convertToDateTimeFormat(self.creation_date, "dateOnly")

    def getCreationDateTime(self):
        return self.convertToDateTimeFormat(self.creation_date)

    def getDueDate(self):
        return self.convertToDateTimeFormat(self.due_date, "dateOnly")

    def getDueDateTime(self):
        return self.convertToDateTimeFormat(self.due_date)
