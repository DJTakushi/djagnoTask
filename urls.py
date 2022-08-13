from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'djangoTask'
urlpatterns = [
    path('', views.index, name='index'),
    path('index/<str:message>', views.index, name='indexM'),
    path('about', views.about, name='about'),
    path('base', views.base, name='base'),
    path('import', views.importData, name='import'),
    path('export', views.exportData, name='export'),
    path('<int:todo_id>/status/', views.status, name='status'),
    path('<int:todo_id>/', views.detailViewNonGeneric, name='detail'),
    path('<int:todo_id>/editPost/', views.editPost, name='editPost'),
    path('delete/', views.deletePost, name='delete'),
    path('createPost', views.editPost, name='createPost'),
    path('new',views.detailViewNonGeneric,name='new'),
    path('accounts/', include('django.contrib.auth.urls')),
]

apiPatterns = [
    path('api/', views.todoList.as_view(), name='api'),
    path('api/<int:pk>/', views.todoDetail.as_view(), name='apiIdx'),
    path('api/users/',views.UserList.as_view()),
    path('api/users/<int:pk>/',views.UserDetail.as_view()),
]
apiPatterns=format_suffix_patterns(apiPatterns)
urlpatterns = urlpatterns+apiPatterns
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
