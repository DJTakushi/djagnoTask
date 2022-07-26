from django.urls import path

from . import views

app_name = 'djangoTask'
urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('base', views.base, name='base'),
    path('import', views.importData, name='import'),
    path('export', views.exportData, name='export'),
    # path('<int:todo_id>/status/', views.index, name='status'),
    # path('<int:todo_id>/', views.index, name='status'),
    # path('<int:todo_id>/editPost/', views.index, name='status'),
    # path('createPost', views.index, name='status'),
    # path('new', views.index, name='status'),

    path('<int:todo_id>/status/', views.status, name='status'),
    # path('<int:pk>/edit/', views.EditView.as_view(), name='edit'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:todo_id>/', views.detailViewNonGeneric, name='detail'),
    path('<int:todo_id>/editPost/', views.editPost, name='editPost'),
    path('createPost', views.editPost, name='createPost'),
    path('new',views.detailViewNonGeneric,name='new'),
]
