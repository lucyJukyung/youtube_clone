from django.shortcuts import render
from django.views.generic.base import View, HttpResponse, HttpResponseRedirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
# Create your views here.

class HomeView(View):
    template_name = "index.html"
    def get(self, request):
        variableA = "some texts"
        return render(request, self.template_name, {'variableA': variableA})


class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # print(request)
        # print(dir(request))
        return HttpResponse("This is Index view. POST Request.")

class RegisterView(View):
    template_name = "register.html"

    def get(self, request):
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
        variableA = "New videos"
        return render(request, self.template_name, {'variableA': variableA})

    def post(self, request):
        return HttpResponse("This is Index view. POST Request.")
