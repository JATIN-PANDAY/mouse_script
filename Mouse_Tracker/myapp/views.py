import re
import pyautogui
import time
import threading
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import User
from datetime import datetime, timedelta

# Create your views here.



# Mouse movement Function


def check_mouse_activity(interval=10):
    last_position = pyautogui.position()
    last_move_time = time.time()

    while True:
        current_position = pyautogui.position()

        if current_position != last_position:
            last_move_time = time.time()
            last_position = current_position
            
        else:
            if time.time() - last_move_time >= interval:
                return False  # Mouse pointer not moved
        time.sleep(1)



# # def check_mouse_activity():
# #     interval = 10  # Time interval to check for mouse activity (in seconds)
# #     last_position = pyautogui.position()
# #     last_move_time = time.time()
# #     try:

# #         while True:
# #             current_position = pyautogui.position()

# #             if current_position != last_position:
# #                 last_move_time = time.time()
# #                 last_position = current_position
# #             else:
# #                 if time.time() - last_move_time >= interval:
# #                     print('not moved')
# #                     # messages.warning(request, 'Your mouse pointer not moved')
# #                     return redirect('/signin')
# #                     break
# #                     last_move_time = time.time()
# #             time.sleep(1)        
        
# #     except KeyboardInterrupt:
# #         print("Timer stopped manually")



# def check_mouse_activity(email):
#     interval = 10  # Time interval to check for mouse activity (in seconds)
#     last_position = pyautogui.position()
#     last_move_time = time.time()

#     try:
#         while True:
#             current_position = pyautogui.position()

#             if current_position != last_position:
#                 last_move_time = time.time()
#                 last_position = current_position
#             else:
#                 if time.time() - last_move_time >= interval:
#                     # Mouse not moved, redirect to signin page
#                     return redirect('signin')
#                     break
#                 last_move_time = time.time()

#             time.sleep(1)
#     except KeyboardInterrupt:
#         print("Timer stopped manually")

def signin(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            user_obj = User.objects.get(email=email)
                
            if user_obj:
                if user_obj.password == password:
                    # Start a new thread to monitor mouse activity
                    thread = threading.Thread(target=check_mouse_activity, args=(email,))
                    thread.start()

                    # Set cookies and redirect to index page
                    response = redirect('index')  # Redirect to the index page
                    response.set_cookie('email', email, max_age=11)  
                    response.set_cookie('password', password, max_age=11)  
                    response.set_cookie('uid', user_obj.uid, max_age=11) 
                    return response
                else:
                    messages.warning(request, 'Incorrect Password')
                    return HttpResponseRedirect(request.path_info)
            else:
                messages.warning(request, 'Invalid credentials')
                return HttpResponseRedirect(request.path_info)
    except User.DoesNotExist:
        messages.warning(request, 'Incorrect Email')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'signin.html')

def index(request):

    uid = request.COOKIES.get('uid')
    if uid:
        if check_mouse_activity():
                        # Mouse activity detected, set cookies
            response = redirect('index')
            response.set_cookie('email', email, max_age=60)  
            response.set_cookie('password', password, max_age=60)  
            response.set_cookie('uid', uid, max_age=60) 
            return response
        else:
                      
            messages.warning(request, 'No mouse activity detected. Please log in again.')
            return HttpResponseRedirect(request.path_info)
        return render(request, 'index.html', {'uid': uid})
    else:
        return redirect('signin')

# Signup

def signup(request):
    if request.method == 'POST':
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword=request.POST.get("cpassword")

        user_obj= User.objects.filter(email=email)
        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)
            
        else:
            if password==cpassword:
                user = User.objects.create(email=email,password=password)
                return redirect('signin')
            else:
                messages.warning(request,"Password and confirm password not match")
                return HttpResponseRedirect(request.path_info)

    return render(request,'signup.html')
        





def signin(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            user_obj = User.objects.get(email=email)
                
            if user_obj:
                if user_obj.password == password:
                    # Check for mouse activity
                    if check_mouse_activity():
                        # Mouse activity detected, set cookies
                        response = redirect('index')
                        response.set_cookie('email', email, max_age=60)  
                        response.set_cookie('password', password, max_age=60)  
                        response.set_cookie('uid', user_obj.uid, max_age=60) 
                        return response
                    else:
                        # No mouse activity, display message or handle as needed
                        messages.warning(request, 'No mouse activity detected. Please log in again.')
                        return HttpResponseRedirect(request.path_info)
                else:
                    messages.warning(request, 'Incorrect Password')
                    return HttpResponseRedirect(request.path_info)
            else:
                messages.warning(request, 'Invalid credentials')
                return HttpResponseRedirect(request.path_info)
    except User.DoesNotExist:
        messages.warning(request, 'Incorrect Email')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'signin.html')


# def signin(request):
#     try:
#         if request.method == 'POST':
            
#             email = request.POST.get('email')
#             password = request.POST.get('password')

#             user_obj = User.objects.get(email = email)
                
#             #profile=Profile.objects.filter(user=user_obj)

#             if user_obj:
#                 if user_obj.password==password:
#                         response= redirect('/')
#                         response.set_cookie('email', email, max_age=60)  
#                         response.set_cookie('password', password, max_age=60)  
#                         response.set_cookie('uid', user_obj.uid, max_age=60) 
#                         return  response
#                 else:
#                     messages.warning(request, 'Incorrect Password')
#                     return HttpResponseRedirect(request.path_info)
#             else:
#                 messages.warning(request, 'Invalid credentials')
#                 return HttpResponseRedirect(request.path_info)
#     except User.DoesNotExist:
#         messages.warning(request, 'Incorrect Email')
#         return HttpResponseRedirect(request.path_info)

#     return render(request, 'signin.html')