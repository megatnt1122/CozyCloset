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
from .forms import Upload, AddToCloset
from .models import clothingStyles, clothingCategories, userClothes, Closet, closetClothes
from django.db.models import Q


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
    user = Post.author

    #Get info from another model
    #Help from https://www.geeksforgeeks.org/how-to-pass-additional-context-into-a-class-based-view-django/
    #Way number 1
    #extra_context ={'userClothes': userClothes.objects.filter(bloguser=self.request.user)}

    #Way number 2
    def get_context_data(self,*args, **kwargs):
        extra_context = super(PostCreateView, self).get_context_data(*args,**kwargs)
        extra_context['userClothes'] = userClothes.objects.filter(bloguser=self.request.user)
        try:
            shareditem = get_object_or_404(userClothes, id=self.kwargs.get('itemid')) # This didn't break
            extra_context['shareditem'] = shareditem
            adding = Post(title=Post.title, content=Post.content, date_posted=Post.date_posted, author=request.user, image='download.jpg') #might need image = and look up about updateing
            adding.save()
        except:
            pass
        return extra_context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    #def get_item(self):
        #shareitemid = get_object_or_404(User, itemid=self.kwargs.get('itemid'))
        #print(shareitemid)
        #return print(shareitemid)


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

class PostAddImgView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'Image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# the view for the upload page
class UploadView(LoginRequiredMixin, CreateView):
    model = userClothes
    fields = ['name','category','style','color','image']

    # only shows the users' closets in the closet drop down when uploading a new item
    #def get_form(self, *args, **kwargs):
    #    form = super(UploadView, self).get_form(*args, **kwargs)
    #    form.fields['closet'].queryset = Closet.objects.filter(closetUser=self.request.user)
    #    return form

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
def myClosets(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        context = {
            'user': request.user,
            'username': username,
            'closets': Closet.objects.filter(closetUser=request.user),
            'title': 'Closets'
        }

        return render(request, 'blog/my_closets.html', context)

@login_required
def userClosets(request, username=None):
    if request.user.is_authenticated:
        user = get_object_or_404(User, username=username)
        context = {
            'user': user,
            'username': username,
            'closets': Closet.objects.filter(closetUser=user),
            'title': 'Closets'
        }

        return render(request, 'blog/user_closets.html', context)

@login_required
def openMyCloset(request, closetid=None):
    username = None
    closet = get_object_or_404(Closet, id=closetid)
    if request.user.is_authenticated:
        username = request.user.username
        if len(closetClothes.objects.filter(closet=closetid)) == 0:
            empty = True
        else:
            empty = False
        clothes = []
        for c in closetClothes.objects.filter(closet=closetid):
            clothes.append(c.clothing_item)
        context = {
            'closet': closet,
            'username': username,
            'closetClothes': clothes,
            'title': closet.name,
            'empty': empty
        }

        return render(request, 'blog/open_my_closet.html', context)

@login_required
def openUserCloset(request, username=None, closetname=None):
    closet = get_object_or_404(Closet, name=closetname)
    user = get_object_or_404(User, username=username)
    if request.user.is_authenticated:
        if len(closetClothes.objects.filter(closet=closet.id)) == 0:
            empty = True
        else:
            empty = False
        clothes = []
        for c in closetClothes.objects.filter(closet=closet.id):
            clothes.append(c.clothing_item)
        context = {
            'closet': closet,
            'username': username,
            'closetClothes': clothes,
            'title': closet.name,
            'empty': empty
        }

        return render(request, 'blog/open_user_closet.html', context)

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
def AddToCloset(request, itemid=None):
    item = userClothes.objects.get(id=itemid)

    if request.POST.get("save"):
        for c in Closet.objects.filter(closetUser=request.user):
            if request.POST.get(str(c.id)) == "clicked":
                adding = closetClothes(closet=c, clothing_item=item, user=request.user)
                adding.save()
        return redirect(reverse('my-clothes'))
    Closets = Closet.objects.filter(closetUser=request.user)
    closets = []
    for c in Closets:
        if len(closetClothes.objects.filter(closet=c, clothing_item=item, user=request.user)) == 0:
            closets.append(c)
    context = {
        'user': request.user,
        'closets': closets,
    }

    return render(request, 'blog/AddToCloset.html', context)

@login_required
def AddToPost(request, itemid=None):
    item = userClothes.objects.get(id=itemid)

    if request.POST.get("save"):
        for c in Closet.objects.filter(closetUser=request.user):
            if request.POST.get(str(c.id)) == "clicked":
                adding = closetClothes(closet=c, clothing_item=item, user=request.user) #Adding to Post
                adding.save()

    Closets = Closet.objects.filter(closetUser=request.user)
    closets = []
    context = {
        'user': request.user,
        'closets': closets, #Make need to change
    }

    return render(request, 'blog/AddToPost.html', context)

@login_required
def deleteItem(request, itemid=None, closetid=None):
    # get item from database
    item = get_object_or_404(userClothes, id=itemid)
    if closetid == None:
        # delete item
        item.delete()
        #return render(request, "blog/user_clothes.html", context)
        return redirect(reverse('my-clothes'))
    else:
        closet = get_object_or_404(Closet, id=closetid)
        closetitem = get_object_or_404(closetClothes, closet=closet, clothing_item=item)
        closetitem.delete()
        return redirect(reverse('open-closet', kwargs={'closetid': closetid}))

@login_required
def deleteCloset(request, closetid=None):
    closet = get_object_or_404(Closet, id=closetid)
    closet.delete()
    return redirect(reverse('my-closets'))
