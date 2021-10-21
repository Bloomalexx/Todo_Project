from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'todo_App/home.html')

def signupuser(request): # Страница регистрации
    if request.method=="GET":
        return render(request, 'todo_App/signupuser.html', {'form_to_authentication': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save() # Сохраняем данные в базу данных
                login(request, user)
                return redirect('currenttodos')

            except IntegrityError:
                return render(request, 'todo_App/signupuser.html',
                              {'form_to_authentication': UserCreationForm(), 'Error':
                                  "That Username has already been taken. Please choose a new Username"})

        else:
            return render(request, 'todo_App/signupuser.html', {'form_to_authentication': UserCreationForm(), 'Error':
                                                                "Passord didn't match"})

@login_required
def currenttodos(request): # Страница задач пользователя
    todos = Todo.objects.filter(user=request.user, date_complited__isnull=True) # Для отоображения записей конкретного пользователя.  date_complited__isnull=True - если задача выполнена, то она исчезает из списка задач
    return render(request, 'todo_App/currenttodos.html', {'todos': todos})

def loginuser(request):
    if request.method == "GET":
        return render(request, 'todo_App/loginuser.html', {'form_login': AuthenticationForm()})  # Перенаправляем пользователя на страницу входа
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo_App/loginuser.html', {'form_login': AuthenticationForm(), 'Error_Login': "Username or password didn't match"})
        else:
            login(request, user)
            return redirect('currenttodos')

def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')

    return render(request, 'todo_App/logoutuser.html')

@login_required
def createtodo(request):
    if request.method == "GET":
        return render(request, 'todo_App/createtodo.html', {'form_createtodo': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST) # Данная форма сохрянет все данные в БД введенные пользователем
            newtodo = form.save(commit=False) # Данная форма сохрянет все данные в БД введенные пользователем
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos') # Перенаправляем пользователя на список записей
        except ValueError:
            return render(request, 'todo_App/createtodo.html', {'form_createtodo': TodoForm(), 'error': 'Your Title so loooong'})

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user) # Отображение задач в соответсвии с авторизированным ползьзователем "user=request.user"
    if request.method == "GET":
        form = TodoForm(instance=todo)
        return render(request, 'todo_App/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo_App/viewtodo.html', {'todo':todo, 'form':form, 'error':'You must change your info'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.date_complited = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

@login_required
def completed_todos(request):
    todos = Todo.objects.filter(user=request.user,
                                date_complited__isnull=False).order_by('-date_complited')  # - перед date_complited означает обратный порядок
    # Для отоображения записей конкретного пользователя.  date_complited__isnull=True - если задача выполнена, то она исчезает из списка задач
    return render(request, 'todo_App/completed_todos.html', {'todos': todos})
