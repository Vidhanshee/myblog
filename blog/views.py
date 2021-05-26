from django.shortcuts import render,redirect,HttpResponseRedirect
from .forms import SignUPForm
from .models import Post
from .forms import CommentForm,LoginForm,PostForm
from  django.contrib import messages
from  django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group
# Create your views here.
def home(request):
    posts = Post.objects.all()
    latest = Post.objects.latest('date_added')
    return render(request,'blog/home.html',{'posts': posts, 'latest':latest})

def About(request):
    return render(request,'blog/About.html')

def Contact(request):
    return render(request,'blog/Contact.html')

def post_detail(request,slug):
    post = Post.objects.get(slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',slug=post.slug)
    else:
        form = CommentForm()
        return render(request, 'blog/post_detail.html', {'post': post, 'form': form})

def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        grp = user.groups.all()
        return render(request, 'blog/dashboard.html', {'posts': posts, 'full_name':full_name, 'groups':grp})
    else:
        return HttpResponseRedirect("/login")


def user_login(request):
    if not request.user.is_authenticated:
        if (request.method == "POST"):
            form = LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname,password=upass)
                print("Login form is valid ")
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in Successfully !!')
                    return HttpResponseRedirect("/dashboard")
                else:
                    form = LoginForm()
                    messages.warning(request, 'Invalid username or password ')
                    return render(request,'blog/login.html', {'form': form})
            else:
                print("Login form is not valid ")
                form = LoginForm()
                messages.warning(request, 'Invalid username or password ')
                return render(request, 'blog/login.html', {'form': form})
        else:
            form = LoginForm()
            return render(request,'blog/login.html', {'form': form})
    else:
        return HttpResponseRedirect("/dashboard")


def user_signup(request):
    if(request.method == "POST"):
        form = SignUPForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulation You have become an Author!')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)

    else:
        form = SignUPForm()
    return render(request,'blog/signup.html',{'form':form})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                slug = form.cleaned_data['slug']
                intro =form.cleaned_data['intro']
                body = form.cleaned_data['body']
                p = Post(title=title,slug=slug,intro=intro,body=body)
                p.save()
                form= PostForm()
                messages.success(request, 'Your Post got Added !')
        else:
            form = PostForm()
        return render(request,'blog/add_post.html',{'form':form})
    else:
        return HttpResponseRedirect("/login")

def update_post(request,slug):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(slug=slug)
            form = PostForm(request.POST,instance=pi)
            form.save()
            messages.success(request, 'Your Post got Updated !')
        else:
            pi = Post.objects.get(slug=slug)
            form = PostForm(instance=pi)

        return render(request, 'blog/update_post.html', {'form': form})
    else:
        return HttpResponseRedirect("/login")

def delete_post(request,slug):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(slug=slug)
            pi.delete()
            return HttpResponseRedirect("/dashboard")
    else:
        return HttpResponseRedirect("/login")