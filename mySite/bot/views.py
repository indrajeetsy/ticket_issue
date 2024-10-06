import random
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as lg
from django.db.models import Q

username = None

def home(request):
    return render(request, 'base.html',{'username':request.user.username})

def get_context(request,data={}):
    data['user_logged_in']=request.user.is_authenticated
    return data

def login(request):
    if request.method=='POST':
        print('post')
        print(request.POST,request.GET)
        user = request.POST.get('username')
        password = request.POST.get('password')
        print(user,password)
        user = authenticate(username=user, password=password)
        print(user)
        if user is not None:
            lg(request, user)
            global username
            username = user
            return redirect('home')
    return render(request,'login.html')
    

def get_username(request):
    global username
    print(username)
    if username is not None:
        return JsonResponse({"logged_in": username.username})
    else:
        return JsonResponse({"logged_in": None})
    
@csrf_exempt
def raise_ticket(request):
    global username
    data = get_context(request)
    if request.method=='POST':
        data = json.loads(request.body)
        issue = data['issue']
        try:
            if username.is_authenticated:
                ticket = Ticket.objects.create(user=User.objects.get(user__username=username.username),issue=issue)
                data['ticket']=ticket.__str__()
                print('data',data)
                return JsonResponse(data)
        except AttributeError as e:
            print(e)
        except User.DoesNotExist:
            User.objects.create(user=username,passkey=random.randint(1000, 9999))
            raise_ticket(request)
        return JsonResponse(None,safe=False)
    
@csrf_exempt
def ticket_status(request):
    global username
    data = get_context(request)
    tickets = [i.__str__() for i in Ticket.objects.filter(Q(user__user=username)&Q(cancelled_by_user=False)).all()]
    data['tickets'] = tickets if tickets!=[] else 'No active tickets.'
    return JsonResponse(data)