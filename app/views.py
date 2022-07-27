
from multiprocessing import context
from django.shortcuts import redirect,render
from .forms import *
from django.views import generic
from .models import HomeWork,Todo
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def Home(request, *args,**kwargs):
    return render(request,'home.html')    
@login_required
def notes(request, *args,**kwargs):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            notes=Notes(user=request.user, title=request.POST.get('title'),description =request.POST.get('description'))
            notes.save()
        messages.success(request,f"Notes added successfully")
    form = NoteForm()
    notes=Notes.objects.filter(user=request.user)
    context={'notes':notes,'form':form}
    return render(request,'notes.html',context)
@login_required    
def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')
@login_required
def detail_note(request,pk=None):
    note = Notes.objects.get(id=pk)
    context ={
        'notes':note
    }
    return render(request,'notes_detail.html',context) 
@login_required     
def Homework(request):
    if request.method == 'POST':
        form = HomeForm(request.POST)
        if form.is_valid():
            finished = request.POST.get('is_finished', None)
            if finished=="on":
                is_finished = True
            else:
                is_finished = False    
            Homework = HomeWork(user=request.user,title = request.POST['title'],subject = request.POST['subject'],description =request.POST['description'],due=request.POST['due'],is_finished=is_finished)
            Homework.save()
    else:
        form = HomeForm()    
    com= None
    home_work = HomeWork.objects.filter(user=request.user)
    if len(home_work)==0:
        com = True
    if len(home_work)==0:
        com = False
    context ={
    'homeworks':home_work,'com':com,'form':form
    }
    return render (request,'homework.html',context) 
@login_required    
def delete_homework(request,pk=None):
      HomeWork.objects.get(id=pk).delete()
      return redirect ('homework')
@login_required      
def updatehomework(request,pk=None):
    homework=HomeWork.objects.get(id=pk)      
    if homework.is_finished==False:
       homework.is_finished=True
    else:
       homework.is_finished=False
    homework.save()
    return redirect('homework')   
def Youtube(request):
    result=[]
    if request.method == 'POST':
        form = Dashform(request.POST)
        text = request.POST['Text']
        video = VideosSearch(text,limit=10)
        for i in video.result()['result']:
            result_dic={
                'title':i['title'],
                'duration':i['duration'],
                'view':i['viewCount']['short'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'publishedTime':i['publishedTime']
            }
            desc=""
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dic['description']=desc
            result.append(result_dic)      
    else:
        form=Dashform()
    context = {'form':form,'results':result}
    return render(request,"youtube.html",context)   
@login_required         
def todo(request):
    if request.method == 'POST':
        form = Todoform(request.POST)
        if form.is_valid():
            try:
                is_finished = request.POST['is_finished']
                if is_finished == True:
                    finished = True
                else:
                    finshed =False
            except:
                finished=False     
                is_finished=finished
            todo=Todo(user=request.user,title=request.POST.get('title'),is_finished = is_finished)
            todo.save()
    else:
        form =Todoform()          
    todo = Todo.objects.filter(user=request.user)
    todo_done = None
    if len(todo) == 0:
        todo_done=True
    else:
        todo_done=False
    form=Todoform()
    context = {'form':form,'todos':todo,'done':todo_done}
    return render(request,"todo.html",context)
@login_required    
def update_todo(request,pk=None): 
    todo = Todo.objects.get(id=pk)      
    if  todo.is_finished==True:
        todo.is_finished=False
    else:
        todo.is_finished=True
    todo.save()
    return redirect('todo')
@login_required    
def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")
            
def books(request):
   
    if request.method == 'POST':
        form = Dashform(request.POST)
        text = request.POST['Text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r= requests.get(url)
        answer = r.json()
        result_list=[]

        for i in range (10):
            result_dic={
                'title':answer ['items'][i]['volumeInfo'].get('title'),
                'subtitle':answer ['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer ['items'][i]['volumeInfo'].get('description'),
                'count':answer ['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer ['items'][i]['volumeInfo'].get('categories'),
                'rating':answer ['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer ['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer ['items'][i]['volumeInfo'].get('previewLink')
                
            }
            result_list.append(result_dic)    
        context = {'form':form,'results':result_list}
        return render(request,'books.html',context)
    else:
        form =  Dashform()
        context={'form':form}
        return render(request,'books.html',context)

def dictionary(request):
    if request.method ==  'POST':
        form= Dashform(request.POST)
        text = request.POST['Text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r = requests.get(url)
        answer = r.json()
        try:
            ph = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['synonyms']
            antonyms = answer[0]['meanings'][0]['antonyms']
            context = {
                'form':form,
                'input':text,
                'ph':ph,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms,
                'antonyms':antonyms,
            }
        except:
            context = {
                'form':form,
                'input':'no word'
            }  
        return render(request,"dictionary.html",context)    
    else:
        form =  Dashform()
        context = {'form':form}
        return render(request,'dictionary.html',context)
def wiki(request):
    if request.method=='POST':
        form= Dashform(request.POST)
        text = request.POST['Text']
        search = wikipedia.page(text)
        summary = wikipedia.summary(text)
        context ={
             'form':form,
             'title':search.title,
             'link':search.url,
             'details':summary }
        return render (request,"wiki.html",context)
    else:
        form = Dashform()
        context = {
            'form':form  
        }
        return render(request,"wiki.html",context)
def conversion(request):
    if request.method == 'POST':
        form = ConversionForm()
        if request.POST['measurement']=='length':
            meas_form = ConversionLengthForm()
            context={
                'form':form,
                'meas_form':meas_form,
                'input':True,
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input  = request.POST['input']
                answer=''
                if input and int(input)>=0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {int(input)*3} foot'
                    if second == 'foot' and second == 'yard':
                        answer=f'{input} foot = {int(input)/3} yard' 
                context = {
                    'form':form,
                    'meas_form':meas_form,
                    'input':True,
                    'answer':answer,
                }          
        if request.POST['measurement']=='mass':
            meas_form = ConversionMassForm()
            context={
                'form':form,
                'meas_form':meas_form,
                'input':True,
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input  = request.POST['input']
                answer=''
                if input and int(input)>=0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound = {int(input)*0.453592} kilogram'
                    if second == 'kilogram' and second == 'pound':
                        answer=f'{input} kilogram = {int(input)*2.20462} pound' 
                context = {
                    'form':form,
                    'meas_form':meas_form,
                    'input':True,
                    'answer':answer,
                }          
    else:
        form=ConversionForm()
    context={
        'form':form,
        'input':False
    }
    return render(request,'conversion.html',context)        
def register(request):
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request,f"account created successfuly")
            return redirect("login")
    else:                
        form=UserRegisterationForm()
    context={
        'form':form
    }   
    return render(request,'register.html',context)
@login_required    
def profile (request):
    homeworks=HomeWork.objects.filter(is_finished=False,user=request.user)
    todos = Todo.objects.filter(is_finished=False,user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done=False
    if len(todos)==0:
        todo_done = True
    else:
        todo_done=False           
    context={
        'todos':todos,
        'homeworks':homeworks,
        'homework_done':homework_done,
        'todo_done':todo_done

    }     
    return render (request,'profile.html',context)
