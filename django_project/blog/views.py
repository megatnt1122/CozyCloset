from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from .forms import Upload
from .models import clothingStyles, clothingCategories, userClothes, Closet


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# the view for the upload page
class UploadView(LoginRequiredMixin, CreateView):
    model = userClothes
    fields = ['name','category','style','color','closet','image']

    # only shows the users' closets in the closet drop down when uploading a new item
    def get_form(self, *args, **kwargs):
        form = super(UploadView, self).get_form(*args, **kwargs)
        form.fields['closet'].queryset = Closet.objects.filter(closetUser=self.request.user)
        return form

    # links the current user to the item being uploaded
    def form_valid(self, form):
        form.instance.bloguser = self.request.user
        return super().form_valid(form)

# the view for creating a new closet
class ClosetCreateView(LoginRequiredMixin, CreateView):
    model = Closet
    fields = ['name']

    # links the current user to the closet being created
    def form_valid(self, form):
        form.instance.closetUser = self.request.user
        return super().form_valid(form)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def list(request):
    return render(request, 'main/list.html', {'title': 'list'})

@login_required
def usersClosets(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        context = {
            'user': request.user,
            'username': username,
            'closets': Closet.objects.filter(closetUser=request.user),
            'title': 'Closets'
        }

        return render(request, 'blog/closets.html', context)

@login_required
def openCloset(request, closetid=None):
    username = None
    closet = get_object_or_404(Closet, id=closetid)
    if request.user.is_authenticated:
        username = request.user.username
        if len(userClothes.objects.filter(closet=closetid)) == 0:
            empty = True
        else:
            empty = False
        context = {
            'closet': closet,
            'username': username,
            'closetClothes': userClothes.objects.filter(closet=closetid),
            'title': closet.name,
            'empty': empty
        }

        return render(request, 'blog/open_closet.html', context)

@login_required
def Clothes(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        if len(userClothes.objects.filter(bloguser=request.user)) == 0:
            empty = True
        else:
            empty = False
        context = {
            'user': request.user,
            'username': username,
            'userClothes': userClothes.objects.filter(bloguser=request.user),
            'title': 'All Clothes',
            'empty': empty
        }

        return render(request, 'blog/user_clothes.html', context)

@login_required
def deleteItem(request, itemid=None, closetid=None):
    # get the item from the database and delete it
    item = get_object_or_404(userClothes, id=itemid)
    item.delete()

    if closetid == None: 
        #return render(request, "blog/user_clothes.html", context)
        return redirect(reverse('user-clothes'))
    else:
        return redirect(reverse('open-closet', kwargs={'closetid': closetid}))

@login_required
def deleteCloset(request, closetid=None):
    closet = get_object_or_404(Closet, id=closetid)
    closet.delete()
    return redirect(reverse('user-closets'))