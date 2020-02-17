from django.shortcuts import render
from django.views.generic.base import View, HttpResponse, HttpResponseRedirect
from .forms import LoginForm, RegisterForm, NewVideoForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Video, Comment
import string, random # for random string
from django.core.files.storage import FileSystemStorage
import os
from wsgiref.util import FileWrapper
import requests
from bs4 import BeautifulSoup

class VideoFileView(View):
    def get(self, request, file_name):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file = FileWrapper(open(BASE_DIR+'/'+file_name, 'rb'))
        response = HttpResponse(file, content_type='video/mp4')
        response['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
        return response

class HomeView(View):
    template_name = "index.html"

    def get(self, request):
        #start beautifulsoup scraping
        URL="https://www.youtube.com"
        result = requests.get(URL)
        soup = BeautifulSoup(result.text, "html.parser")
        div_s = soup.findAll('div', class_= 'yt-lockup')
        rsSet = []

        for test in div_s:
            rsSet.append(test)

        num_of_block = len(rsSet) #extracted number of video blocks
        block = rsSet
        print(num_of_block)

        #start scraping contents from each block
        def extract_detail(html):
            title = html.find('div', class_= 'yt-lockup-content').find("a")["title"]
            channel = html.find('div', class_= 'yt-lockup-content').find("div", class_= 'yt-lockup-byline').text
            link = html.find('div', class_= 'yt-lockup-content').find("a")["href"]
            views_dates = html.find('div', class_= 'yt-lockup-content').findAll("li")

            view_list=[]
            for li in views_dates:
                view_list.append(li.text)

            image = html.find("span", class_="yt-thumb-simple").find("img")["src"]
            if "https://" not in image:
                image = html.find("span", class_="yt-thumb-simple").find("img")["data-thumb"]

            video_time = html.find("span", class_="yt-thumb-simple").find("span").text

            return {
                'title': title,
                'channel': channel,
                'views': view_list[0],
                'date': view_list[1],
                'link': f"{URL}{link}",
                'image': image,
                'video_time': video_time
            }

        def extract_videos(num_of_block):
            contents = []

            for i in range(num_of_block):
                content = block[i].findAll('div', class_='yt-lockup-dismissable')
                for details in content:
                    block_content = extract_detail(details)
                    contents.append(block_content)

            return contents

        video_list = extract_videos(num_of_block)

        return render(request, self.template_name, {'menu_active_item': 'home', 'video_list': video_list})

class Trending(View):
    template_name = "trending.html"
    def get(self, request):
        #start beautifulsoup scraping
        URL="https://www.youtube.com/feed/trending"
        result = requests.get(URL)
        soup = BeautifulSoup(result.text, "html.parser")
        div_s = soup.findAll('div', class_= 'yt-lockup')
        rsSet = []

        for test in div_s:
            rsSet.append(test)

        num_of_block = len(rsSet) #extracted number of video blocks
        block = rsSet
        print(num_of_block)

        #start scraping contents from each block
        def extract_detail(html):
            title = html.find('div', class_= 'yt-lockup-content').find("a")["title"]
            channel = html.find('div', class_= 'yt-lockup-content').find("div", class_= 'yt-lockup-byline').text
            link = html.find('div', class_= 'yt-lockup-content').find("a")["href"]
            views_dates = html.find('div', class_= 'yt-lockup-content').findAll("li")
            description = html.find('div', class_='yt-lockup-description').text

            view_list=[]
            for li in views_dates:
                view_list.append(li.text)

            image = html.find("span", class_="yt-thumb-simple").find("img")["src"]
            if "https://" not in image:
                image = html.find("span", class_="yt-thumb-simple").find("img")["data-thumb"]

            video_time = html.find("span", class_="yt-thumb-simple").find("span").text

            return {
                'title': title,
                'channel': channel,
                'views': view_list[0],
                'date': view_list[1],
                'link': f"https://www.youtube.com{link}",
                'image': image,
                'video_time': video_time,
                'description': description
            }

        def extract_videos(num_of_block):
            contents = []

            for i in range(num_of_block):
                content = block[i].findAll('div', class_='yt-lockup-dismissable')
                for details in content:
                    block_content = extract_detail(details)
                    contents.append(block_content)

            return contents

        trending_list = extract_videos(num_of_block)

        return render(request, self.template_name, {'trending_list': trending_list})

class MyVideoView(View):
    template_name = "my_videos.html"
    def get(self, request):
        # fetch video from DB
        most_recent_videos = Video.objects.order_by('-datetime')[:10] # desc order (-)
        print(most_recent_videos)
        #most_recent_videos[5] = {'extraarea':}

        return render(request, self.template_name, {'menu_active_item': 'my_videos', 'most_recent_videos': most_recent_videos})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')

class VideoView(View):
    template_name = "video.html"

    def get(self, request, id):
        print(request)
        print('VIDEO ID: {}'.format(id))
        # print(dir(request))
        # DoesNotExist
        # fetch video from DB by ID
        video_by_id = Video.objects.get(id=id)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        video_by_id.path = 'http://localhost:8000/get_video/'+video_by_id.path
        context = {'video': video_by_id}

        print(request.user)
        print(video_by_id.path)

        if request.user.is_authenticated:
            print('User signed in')
            comments_form = CommentForm()
            context['form'] = comments_form

        comments = Comment.objects.filter(video__id=id).order_by('-datetime')[:5]
        print(comments)

        context['comments'] = comments
        return render(request, self.template_name, context)


class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        if request.user.is_authenticated:
            # Do something for authenticated users.
            print("already logged in. redirecting")
            print(request.user) #to see who is logged in.
            # logout(request)
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
                return HttpResponseRedirect('/')
            else:
                print("authentication failed")
                return HttpResponseRedirect('login')
                #if login fails, redirect to login page
        return HttpResponse('This is login view. POST request.')

class CommentView(View):
    template_name = "comment.html"

    def post(self, request):
        # pass filled out html form View to NewVideoForm()
        form = CommentForm(request.POST)

        # check if the the form is valid
        if form.is_valid():
            # create a comment entry
            text = form.cleaned_data['text']

            print(dir(request))
            print(form.data)

            print(request.POST)
            print(dir(form))
            video_id = request.POST['video']
            video = Video.objects.get(id=video_id)

            new_comment = Comment(text=text, user=request.user, video=video)
            new_comment.save()

            print(new_comment)

            return HttpResponseRedirect('/video/{}'.format(str(video_id)))

        return HttpResponse("This is Comment view post request")


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
            return HttpResponseRedirect('/')
        form = NewVideoForm()

        STATICFILES_DIRS = (os.path.join( os.path.dirname( __file__ ), 'static' ),)
        print(STATICFILES_DIRS)

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

            fs = FileSystemStorage(location = os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            filename = fs.save(path, file)
            file_url = fs.url(filename)

            print(fs)
            print(filename)
            print(file_url)

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
