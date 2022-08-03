from django.urls import include, path
from . import views

app_name = 'djangoTask'
urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('base', views.base, name='base'),
    path('import', views.importData, name='import'),
    path('export', views.exportData, name='export'),
    path('<int:todo_id>/status/', views.status, name='status'),
    path('<int:todo_id>/', views.detailViewNonGeneric, name='detail'),
    path('<int:todo_id>/editPost/', views.editPost, name='editPost'),
    path('<delete/', views.deletePost, name='delete'),
    path('createPost', views.editPost, name='createPost'),
    path('new',views.detailViewNonGeneric,name='new'),
    path('api/', views.todo_list, name='api'),
    path('api/<int:pk>/', views.todo_detail, name='apiIdx'),
]
