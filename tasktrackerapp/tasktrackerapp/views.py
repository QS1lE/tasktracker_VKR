from django.shortcuts import render, redirect
from .models import Task, Project
from .forms import CreateTask, CreateProject
from django.urls import reverse 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.utils.formats import localize

from .forms import RegisterUserForm

# Эта функция создаёт словарь проектов и их задач вида {Проект: [Задача 1, задача 2, задача 3]}
def create_dictionary(sort_by=None):
    projects = Project.objects.all()
    project_task_dict = {}

    for project in projects:
        if sort_by:
            tasks = Task.objects.all().filter(project=project).order_by(sort_by)
        else:
            tasks = Task.objects.filter(project=project)
        project_task_dict[project] = list(tasks)
        print(project_task_dict)
    return project_task_dict

# Create your views here.
# Страница с таблицей всех задач
def all_tasks(request):
    data_of_tasks = Task.objects.all()
    sort_by = request.GET.get('sort_by')
    # Если нет метода сортировки, то порядок как в БД. Если есть метод и это не порядок из БД, происходит сортировка
    if request.method == "GET":
        if sort_by == 'None' or sort_by is None:
            sort_by = 'Порядок из БД'
        elif sort_by != 'Порядок из БД':
            if sort_by == 'project': #Нужно отдельно прописать сортировку для названий проекта, так как .order_by просортировала бы по id проектов
                data_of_tasks = Task.objects.all().order_by('project__name')
            else:
                data_of_tasks = Task.objects.all().order_by(sort_by)
    # Обработка POST запросов для создания, удаления или изменения задач, а также для применения сортировки к таблице задач
    elif request.method == "POST":
        if 'createTask' in request.POST:
            return redirect(reverse('create_edit_page') + '?prev_page=/home')
        elif 'deleteTask' in request.POST:
            task_id = request.POST.get('deleteTask')
            task_to_delete = Task.objects.get(id=task_id)
            task_to_delete.delete()
        elif 'editTask' in request.POST:
            task_id = request.POST.get('editTask')
            return redirect(reverse('create_edit_page') + f'?task_id={task_id}&sort_by={sort_by}&prev_page=/home')
        elif 'orderTasks' in request.POST:
            sort_by = request.POST.get('orderTasks')
            return redirect(reverse('all_tasks_page') + f'?sort_by={sort_by}')

    context = {'data': data_of_tasks,
               'sort_by': sort_by,
               }
    return render(request, 'all_tasks.html', context)

 # Страница с карточами проектов
def tasks_by_projects(request):
     # Применение методов сортировки к словарю с проектами и их задачами
    sort_by = request.GET.get('sort_by')
    dict_of_projects = {}
    if request.method == "GET":
        if sort_by == 'None' or sort_by is None:
            sort_by = 'Порядок из БД'
            dict_of_projects = create_dictionary()
        elif sort_by != 'Порядок из БД':
            if sort_by == 'project':
                dict_of_projects = create_dictionary('project__name')
            else:
                dict_of_projects = create_dictionary(sort_by)

    data_of_tasks = Task.objects.all()
    data_of_projects = Project.objects.all()

    context = {
        'tasks': data_of_tasks,
        'projects': data_of_projects,
        'dict_of_projects': dict_of_projects,
        'sort_by': sort_by,
    }
    # Обработка POST запросов для создания, изменения и удаления проекта, 
    # а также для добавления в проект, изменения, удаления и сортировки задач
    if request.method == "POST":
        if 'createProject' in request.POST:
            return redirect('create_project_page')
        elif 'editProject' in request.POST:
            project_id = request.POST.get('editProject')
            prev_page = 'projects'
            return redirect(reverse('create_project_page') + f'?project_id={project_id}&sort_by={sort_by}')
        elif 'deleteProject' in request.POST:
            project_id = request.POST.get('deleteProject')
            project_to_delete = Project.objects.get(id=project_id)
            project_to_delete.delete()
            return redirect('projects_page')
        elif 'deleteTask' in request.POST:
            task_id = request.POST.get('deleteTask')
            task_to_delete = Task.objects.get(id=task_id)
            task_to_delete.delete()
            return redirect('projects_page')
        elif 'editTask' in request.POST:
            task_id = request.POST.get('editTask')
            prev_page = '/projects'
            return redirect(reverse('create_edit_page') + f'?task_id={task_id}&prev_page={prev_page}&sort_by={sort_by}')
        elif 'orderTasks' in request.POST:
            sort_by = request.POST.get('orderTasks')
            return redirect(reverse('projects_page') + f'?sort_by={sort_by}')
        elif 'addTask' in request.POST:
            project_id = request.POST.get('addTask')
            prev_page = '/projects'
            return redirect(reverse('create_edit_page') + f'?project_id={project_id}&prev_page={prev_page}&sort_by={sort_by}')

    return render(request, 'tasks_by_project.html', context)


# Функция для страницы для создания/изменения задач
def create_task(request):
    # При наличии в request id задачи или проекта можно предзаполнить форму/загрузить форму для изменения задачи
    # prev_page содержит информацию о странице, покинутой пользовтаелем перед открытием страницы создания/изменения задач
    # sort_by содержит информацию о методе сорировки с той страницы 
    task_id = request.GET.get('task_id')
    project_id = request.GET.get('project_id')
    prev_page = request.GET.get('prev_page')
    sort_by = request.GET.get('sort_by')
    # Если нет информации о id задачи/проекта, создаётся форма для создания задачи с нуля 
    # (при наличи id проекта, предзаполнен проект)
    # Если есть id задачи, это форма для изменения задачи
    if request.method == "GET":
        if not task_id:
            if not project_id:
                form_create_task = CreateTask()
            else:
                form_create_task = CreateTask(initial={'project': project_id})
            context = {'form_create': form_create_task,
                       'header': 'Создание новой задачи',
                       'prev_page': prev_page}
        else:
            task_to_edit = Task.objects.get(id=task_id)
            form_edit_task = CreateTask(instance=task_to_edit)
            context = {'form_edit': form_edit_task,
                       'header': 'Измените данные задачи',
                       'prev_page': prev_page}
        
        return render(request, 'create_edit_form.html', context)
    # Обработка POST запросов для сохранения данных, указанных в форме
    elif request.method == "POST":
        prev_page = request.GET.get('prev_page')
        if 'save' in request.POST:
            data = request.POST.copy()
            # Выставляем статус "Не указан", если его не выбрали
            if data['status'] == '':
                data['status'] = '5'
            # Подгоняем формат из формы к формату, удобному для сохранения данных в модели
            for date in ['deadline', 'reminder']:
                data[date] = data[date].replace('T', ' ')
            # Если нет id задачи, то создаётся новая задача, иначе изменяем данные в существующей
            if not task_id:
                form_create_task = CreateTask(data)
            else:
                task_to_edit = Task.objects.get(id=task_id)
                form_create_task = CreateTask(data, instance=task_to_edit)
            if form_create_task.is_valid():
                form_create_task.save()
            # Если есть информация о странице, с которой была открыта форма, возвращаемся на неё
            # Иначе возвращаемся на страницу с таблицей всех задач (по возможности, с сохранением способа сортировки)
            if prev_page is not None:
                return redirect(prev_page)
            else:
                return redirect(reverse('all_tasks_page') + f'?sort_by={sort_by}')

# Функция для страницы для создания/изменения проектов
def create_project(request):
    # id проекта нужен для открытия формы изменения проекта, если его нет - создаётся новый проект
    project_id = request.GET.get('project_id')
    if request.method == "GET":
        if not project_id:
            form_create_project = CreateProject()
            context = {'form_create': form_create_project,
                       'header': 'Создание нового проекта',
                       'prev_page': '/projects'}
        else:
            project_to_edit = Project.objects.get(id=project_id)
            form_edit_project = CreateProject(instance=project_to_edit)
            context = {'form_edit': form_edit_project,
                       'header': 'Измените данные проекта',
                       'prev_page': '/projects'}
        return render(request, 'create_edit_form.html', context)
    # Обработка POST запросов для сохранения данных, указанных в форме
    elif request.method == "POST":
        data = request.POST.copy()
        # Если не заполнено описание проекта, заполняется 'Нет описания проекта'
        if data['description'] == '':
            data['description'] = 'Нет описания проекта'
        # Если нет id проекта, создаётся новый проект
        # Если id есть, то изменяется существующий
        if not project_id:
            form_of_project = CreateProject(data)
        else:
            project_to_edit = Project.objects.get(id=project_id)
            form_of_project = CreateProject(data, instance=project_to_edit)
        if form_of_project.is_valid():
            form_of_project.save()
        return redirect('/projects')

# Функция для страницы просмотра информации о задаче по её id
def task_info(request, task_id, prev_page=None):
    task = Task.objects.get(id=task_id)
    prev_page = request.GET.get('prev_page')
    context = {'task': task,
               'task_id': task_id,
               'prev_page': prev_page}
    # Обработка POST запросов для удаления задачи, и для перехода к странице с формой изменения информации о задаче
    if request.method == "POST":
        if 'editTask' in request.POST:
            prev_page = request.POST.get('prev_page')
            task_id = request.POST.get('editTask')
            return redirect(reverse('create_edit_page') + f'?task_id={task_id}&prev_page={prev_page}')
        elif 'deleteTask' in request.POST:
            prev_page = request.POST.get('prev_page')
            task_id = request.POST.get('deleteTask')
            task_to_delete = Task.objects.get(id=task_id)
            task_to_delete.delete()
            return redirect(prev_page)

    return render(request, 'task_info.html', context)

#функция для открытия информации о трекере
def about(request):
    return render(request, 'about.html')

def nullboard(request):
    return render(request, 'nullboard.html') 

def calendar(request):
    return render(request, 'calendar.html' )

# def login_request(request):
#     form = request.GET.get('form')
#     if request.method == 'GET':
#         form = AuthenticationForm(request, data=request.GET)
#         # if not form:
#         #     context = {
#         #         'username': 'Введите пользователя',
#         #         'paswword': 'Введите пароль',
#         #         'prev_page': '/login'
#         #     }
#         return render(request, 'login.html')

# Функция авторизации на сайт
def login_request(request,form):
    context={'login_form': form}
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request,
                              f'Вы вошли на сайт под ником {username}.')
                return redirect('board:home')
            else:
                messages.error(request, 'Неверные имя и/или пароль.')
        else:
            messages.error(request, 'Неверные имя и/или пароль.')
    form = AuthenticationForm()
    return render(request, 'login.html', context)

# Функция регитсрации пользователя
def register_request(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request,
                             'Аккаунт зарегистрирован: '
                             'добро пожаловать на сайт!')
            return redirect('board:login')
        messages.error(request, 'Не удалось зарегистрировать аккаунт. '
                                'Проверьте корректность данных и '
                                'попробуйте еще раз!')
    form = RegisterUserForm()
    return render(request=request,
                  template_name='register.html',
                  context={'register_form': form})



# # Функция перенаправления на главный экран
# # @login_required
# def home(request):
#     all_tasks = []
#     t_list = request.user.tasks.all()
#     for t in t_list:
#         t_dict = {
#             'uuid': str(t.uuid),
#             'name': t.name if t.name is not None else 'Без названия',
#             'boardName': t.boardName,
#             'date': str(localize(t.date))
#         }
#         all_tasks.append(t_dict)
#     return render(request, 'index.html', {'tasks': all_tasks})

# # # Функция выхода с сайта
# # def logout_request(request):
# #     logout(request)
# #     messages.info(request, 'Вы вышли из аккаунта.')
# #     return redirect('board:login')
