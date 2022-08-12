from rest_framework import status as statusRF
from rest_framework import mixins, generics
from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse, Http404
from .models import todo, todoManager, jsonExample, dictToString, jsonExampleImportString
from django.views import generic
from django.urls import reverse
from django.utils import timezone
import json
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .serializers import todoSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import permissions
# from .permissions import IsOwnerOrReadOnly
def returnForbiddenPriviledge(request, msg = None):
    template = loader.get_template('djangoTask/forbidden.html')
    context = {}
    if msg:
        context = {'message' : msg}
    return HttpResponseForbidden(template.render(context,request))


def index(request, message=None):
    todo_list = todo.objects.order_by('creation_date')
    template = loader.get_template('djangoTask/index.html')
    context = {
        'latest_todo_list':todo_list,
    }
    if message:
        context['message'] = message
    return HttpResponse(template.render(context,request))
def base(request):
    template = loader.get_template('djangoTask/base.html')
    context = {}
    return HttpResponse(template.render(context,request))
def about(request):
    template = loader.get_template('djangoTask/about.html')
    context = {}
    return HttpResponse(template.render(context,request))
def importData(request):
    template = loader.get_template('djangoTask/import.html')
    inData=""
    context={}
    if 'inData' in request.POST:
        inData=request.POST['inData']
        requiredPerm = 'djangoTask.add_todo'
        if request.user.has_perm(requiredPerm):
            reply=todo.objects.createFromJson(inData)
            context['message']="reply: "+reply
            context['dataProvided']=inData
        else:
            return returnForbiddenPriviledge(request,  "Request requires permission: "+requiredPerm)
    else:
        context['message']="Input data in text box or by upload (example below)"
        # context['dataProvided']=jsonExample
    context['example']=jsonExampleImportString

    return HttpResponse(template.render(context,request))

def exportData(request):
    template = loader.get_template('djangoTask/export.html')
    context = {}
    export = ""
    try:
        export = todo.objects.getJson()
    except:
        export = "failed to get export data"
    context['export']=export
    return HttpResponse(template.render(context,request))

# Generic views work, but I think the offer less control
# class DetailView(generic.DetailView):
#     model = todo
#     template_name = 'todo/detail.html'

# class EditView(generic.DetailView):
#     model = todo
#     template_name = 'todo/edit.html'

def detailViewNonGeneric(request, todo_id=None):
    context = {
        'todo_id':None,
        'todo_title':"NEW",
        'todo_description':"",
        'todo_creation_date':timezone.now().strftime('%Y-%m-%dT%H:%M'),
        'todo_due_date':timezone.now().strftime('%Y-%m-%dT%H:%M'),
        'todo_status':"open",
        'todo_tags':"",
        'navLink':"new",
        'createPerm': request.user.has_perm('djangoTask.add_todo'),
        'changePerm': request.user.has_perm('djangoTask.change_todo'),
    }
    if todo_id != None:
        todo_t = get_object_or_404(todo, pk=todo_id)
        context['todo_id']=todo_t.id
        context['todo_title']=todo_t.title
        context['todo_description']=todo_t.description
        try:
            context['todo_creation_date']=todo_t.creation_date.strftime('%Y-%m-%dT%H:%M')
        except:
            context['todo_creation_date']=""

        try:
            context['todo_due_date']=todo_t.due_date.strftime('%Y-%m-%dT%H:%M')
        except:
            context['todo_due_date']=""

        context['todo_status']=todo_t.status
        context['todo_tags']=todo_t.tags
        context['todo_owner']=todo_t.owner
        context['ownerList']=User.objects.all()
        context['navLink']=""


    template = loader.get_template('djangoTask/detailNonGeneric.html')
    return HttpResponse(template.render(context,request))

def status(request, todo_id):
    return HttpResponse("You're looking at todo %s." % todo_id)

def editPost(request, todo_id=None):
    context = {}
    context['msg'] = ""
    requiredPerm = 'djangoTask.add_todo'
    if todo_id == None:
        if request.user.has_perm(requiredPerm):
            todo_t = todo()
            todo_t.setTitle(request.POST['title'])
            todo_t.setDescription(request.POST['description'])
            todo_t.setCreationDateFromString(request.POST['creationDate'])
            todo_t.setDueDateFromString(request.POST['dueDate'])
            todo_t.setStatus(request.POST['status'])
            todo_t.setTags(request.POST['tags'])
            todo_t.setOwner(request.POST['owner'])
            todo_t.save()
        else:
            return returnForbiddenPriviledge(request,  "Request requires permission: "+requiredPerm)
    else:
        if request.user.has_perm(requiredPerm):
            todo_t = get_object_or_404(todo, pk=todo_id)
            todo_t.setTitle(request.POST['title'])
            todo_t.setDescription(request.POST['description'])
            todo_t.setCreationDateFromString(request.POST['creationDate'])
            todo_t.setDueDateFromString(request.POST['dueDate'])
            todo_t.setStatus(request.POST['status'])
            todo_t.setTags(request.POST['tags'])
            todo_t.setOwner(request.POST['owner'])
            todo_t.save()
        else:
            return returnForbiddenPriviledge(request,  "Request requires permission: "+requiredPerm)
    message_t = "edit complete"
    return HttpResponseRedirect(reverse('djangoTask:indexM',  kwargs={'message': message_t}))

def deletePost(request):
    message = None
    try:
        todo_t = get_object_or_404(todo, pk=request.POST['todo_id'])
        requiredPerm = 'djangoTask.delete_todo'
        if request.user.has_perm(requiredPerm):
            id_s = todo_t.id
            todo_t.delete()
            message = "Deleted Todo with PK:"+str(id_s)
        else:
            return returnForbiddenPriviledge(request,  "Request requires permission: "+requiredPerm)
    except:
        message = "Deleted Todo with PK:"+str()
    return HttpResponseRedirect(reverse('djangoTask:indexM', kwargs={"message":message}))

class todoList(generics.ListCreateAPIView):
    """
    List all todos, or create a new todo.
    """
    queryset = todo.objects.all()
    serializer_class=todoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)
class todoDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a code todo.
    """
    queryset = todo.objects.all()
    serializer_class=todoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
