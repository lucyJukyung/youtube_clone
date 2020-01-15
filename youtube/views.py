from django.shortcuts import render
from django.views.generic.base import View, HttpResponse, HttpResponseRedirect
from .forms import LoginForm, RegisterForm, NewVideoForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Video, Comment
import string, random

class HomeView(View):
    template_name = "index.html"
    def get(self, request):
        variableA = "some texts"
        return render(request, self.template_name, {'variableA': variableA})


class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        if request.user.is_authenticated:
            # Do something for authenticated users.
            print("already logged in. redirecting")
            print(request.user) #to see who is logged in.
            logout(request)
            return HttpResponseRedirect('new_video')

        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # print(request)
        # print(dir(request))
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            #need a special function bc psswrd is encrypted in db
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user) #this login creates the cookie for user to stay logged in.
                #request will have a value (user) inside.
                print("authentication success")
                # or create a new entry in a table to store logs
                return HttpResponseRedirect('HomeView')
            else:
                print("authentication failed")
                return HttpResponseRedirect('login')
                #if login fails, redirect to login page
        return HttpResponse('This is login view. POST request.')

class RegisterView(View):
    template_name = "register.html"

    def get(self, request):
        if request.user.is_authenticated:
            # Do something for authenticated users.
            print("already logged in. redirecting")
            print(request.user) #to see who is logged in.
            return HttpResponseRedirect('new_video')
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # pass filled out html form
        form = RegisterForm(request.POST)
        # check if the the form is valid
        if form.is_valid():
            #create an account
            print(form.cleaned_data['username'])
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            # check_email = User.objects.get(email=email)
            # if check_email is not None:
            #     return "Entered email already exists!"

            print(username)
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            print(username)
            new_user.save()
            print(username)
            return HttpResponseRedirect('/login')
        print("Hello there Register Post!")
        return HttpResponse("This is Index view. POST Request.")


class NewVideo(View):
    template_name = "new_video.html"

    def get(self, request):
        print(request.user.is_authenticated)
        if request.user.is_authenticated == False:

            # return HttpResponse("You have to login in order to upload a video")
            return HttpResponseRedirect('HomeView')
        form = NewVideoForm()

        variableA = "New videos"
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # pass filled out html form View to NewVideoForm()
        form = NewVideoForm(request.POST, request.FILES)
        print(form)
        print(request.POST)
        print(request.FILES)

        # check if the the form is valid
        if form.is_valid():
            # create a new video entry
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            file = form.cleaned_data['file']
            print(dir(file)) # print data types to find file name ext.
            print(file.name) # confirm with file.name to see if it is printing actual file name

            # creating random string to add in file name to prevent crashing by uploading files under same name
            # k=10 means 10 characters
            random_char = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            path = random_char + file.name # This will prevent same file name upload

            new_video = Video(title=title,
                              description=description,
                              path=path,
                              user=request.user)
            new_video.save()

            print(new_video)

            # redirect to detail view template of a Video
            return HttpResponseRedirect('/video/{}'.format(new_video.id))
        else:
            return HttpResponse("Your form is not valid. Go back and try again.")
