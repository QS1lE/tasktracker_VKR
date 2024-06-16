from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.all_tasks, name='all_tasks_page'), #страница с таблицей всех задач
    path('projects/', views.tasks_by_projects, name='projects_page'),  #страница с карточками проектов
    path('about/',views.about,  name='about_page'),  #страница о трекере
    path('form/', views.create_task, name='create_edit_page'),  #страница с формой для создания/измнения задач
    path('create_project/', views.create_project, name='create_project_page'), #страница для создания/изменения проектов
    path('task_info/<int:task_id>/', views.task_info, name='task_info_page'),  #страница с информацией о конкретной задаче
    path('register/', views.register_request, name='register_page'), #страница для создания пользователей
    # path('login/', views.login_request, name='login_page'), #страница для входа пользователя
    path('login/', views.login_request, name='login_page' ),
    path('nullboard/', views.nullboard, name='nullboard'),
    path('calendar/', views.calendar, name='calendar'),
] 