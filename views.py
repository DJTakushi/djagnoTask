from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse, HttpResponseRedirect
from .models import todo
from django.views import generic
from django.urls import reverse
from django.utils import timezone

from django.template import loader

def index(request):
    todo_list = todo.objects.order_by('creation_date')
    template = loader.get_template('djangoTask/index.html')
    context = {
        'latest_todo_list':todo_list,
    }
    return HttpResponse(template.render(context,request))
def base(request):
    template = loader.get_template('djangoTask/base.html')
    context = {}
    return HttpResponse(template.render(context,request))
def about(request):
    template = loader.get_template('djangoTask/about.html')
    context = {}
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
        'todo_status':"",
        'todo_tags':"",
    }
    if todo_id != None:
        print("todo_id = ",todo_id)
        todo_t = get_object_or_404(todo, pk=todo_id)
        context['todo_id']=todo_t.id
        context['todo_title']=todo_t.title
        context['todo_description']=todo_t.description
        context['todo_creation_date']=todo_t.getCreationDateTime()
        context['todo_due_date']=todo_t.getDueDateTime()
        context['todo_status']=todo_t.status
        context['todo_tags']=todo_t.tags

    template = loader.get_template('djangoTask/detailNonGeneric.html')
    return HttpResponse(template.render(context,request))

def status(request, todo_id):
    return HttpResponse("You're looking at todo %s." % todo_id)

def editPost(request, todo_id=None):
    if todo_id == None:
        todo_t = todo()
        todo_t.title = request.POST['title']
        todo_t.description = request.POST['descriptionPost']
        todo_t.creation_date = request.POST['creationDatePost']
        todo_t.due_date = request.POST['dueDatePost']
        todo_t.status = request.POST['statusPost']
        todo_t.tags = request.POST['tagsPost']
        todo_t.save()
    else:
        todo_t = get_object_or_404(todo, pk=todo_id)
        todo_t.title = request.POST['title']
        todo_t.description = request.POST['descriptionPost']
        todo_t.creation_date = request.POST['creationDatePost']
        todo_t.due_date = request.POST['dueDatePost']
        todo_t.status = request.POST['statusPost']
        todo_t.tags = request.POST['tagsPost']
        todo_t.save()
    return HttpResponseRedirect(reverse('djangoTask:index'))
