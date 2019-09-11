from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Todo
from decouple import config
import telegram
import requests
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

synastry = config("synastrybot")
angi = config("angi_bot")
park = config("park")
jimmy = config("jimmy")

def index(request):
    todos = Todo.objects.all()
    context = {
        'todos': todos,
    }
    return render(request, 'todos/index.html', context)

# def new(request):
#     return render(request, 'todos/new.html')

def create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        due_date = request.POST.get('due-date')

        Todo.objects.create(
            title=title, 
            due_date=due_date
        )
        synastry_bot = telegram.Bot(token = synastry)
        angi_bot = telegram.Bot(token = angi)
        synastry_bot.sendMessage(chat_id = park, text=f"todo: {title} due_date: {due_date}")
        angi_bot.sendMessage(chat_id = park, text=f"todo: {title} due_date: {due_date}")
        synastry_bot.sendMessage(chat_id = jimmy, text=f"todo: {title} due_date: {due_date}")
        angi_bot.sendMessage(chat_id = jimmy, text=f"todo: {title} due_date: {due_date}")
        return redirect('todos:index')
        
    else:
        return render(request, 'todos/create.html')

def update(request, pk):
    # todo = Todo.objects.get(id=pk)
    todo = get_object_or_404(Todo, id=pk)
    context = {
        'todo': todo
    }
    if request.method == "POST":
        title = request.POST.get('title')
        due_date = request.POST.get('due-date')

        todo.title = title
        todo.due_date = due_date
        todo.save()
        base_url = "https://api.telegram.org/bot"
        for bot in [synastry, angi]:
            for user in [park, jimmy]:
                url = base_url + f'{bot}/sendMessage?text=title: {title} due date: {due_date}&chat_id={user}'
                requests.post(url)
        return redirect('todos:index')
        

    else:
        return render(request, 'todos/update.html', context)

def delete(request, pk):
    todo = get_object_or_404(Todo, id=pk)
    todo.delete()

    return redirect('todos:index')

csrf_exempt
def telegram(request):
    print(request.method)
    print(request)
    return HttpResponse("Goooood!")