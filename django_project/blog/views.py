from django.shortcuts import render, get_object_or_404, redirect, reverse
from collections import defaultdict
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from .forms import *
from .models import *
from django.db.models import Q

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)])) #ThIS IS PROBABLY WRONG

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
    
    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args,**kwargs)
        
        
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["total_likes"] = total_likes
        context["liked"] = liked
        return context

class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/add_comment.html'
    #fields = '__all__'
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.name = self.request.user
        return super().form_valid(form)
    success_url = reverse_lazy('blog-home')

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']

    def dispatch(self, request, *args, **kwargs):
        self.item = kwargs.get('itemid', "")
        return super(PostCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self,*args, **kwargs):
        extra_context = super(PostCreateView, self).get_context_data(*args,**kwargs)
        extra_context['userClothes'] = userClothes.objects.filter(bloguser=self.request.user)
        if 'itemid' in self.kwargs:
            shareditem = userClothes.objects.filter(id=self.kwargs['itemid']).first()
            if shareditem:
                extra_context['shareditem'] = shareditem
        return extra_context

    def form_valid(self, form):
        post = form.save(commit=False)  # Save the form to the 'post' but don't commit to the database yet
        post.author = self.request.user
        if 'itemid' in self.kwargs:  # Check if 'itemid' was passed to the view
            shareditem = userClothes.objects.filter(id=self.kwargs['itemid']).first()
            if shareditem:  # Check if a valid userClothes item was found
                post.image = shareditem.image  # Assign the image from the shareditem to the post instance
        post.save()  # Now save the post to the database
        return HttpResponseRedirect(post.get_absolute_url())  # Redirect to the newly created post's detail view


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']

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
    fields = ['name','category','style','color','image']

    # links the current user to the item being uploaded
    def form_valid(self, form):
        form.instance.bloguser = self.request.user
        return super().form_valid(form)

# the view for creating a new closet
class ClosetCreateView(LoginRequiredMixin, CreateView):
    model = Closet
    fields = ['name', 'is_public']

    # links the current user to the closet being created
    def form_valid(self, form):
        form.instance.closetUser = self.request.user
        return super().form_valid(form)

# The view for editing a closet
class ClosetUpdateView(LoginRequiredMixin, UpdateView):
    model = Closet
    fields = ['name', 'is_public']
    template_name = 'blog/closet_edit.html'

    def get_success_url(self):
        return reverse('my-closets')

    def get_object(self):
        return get_object_or_404(Closet, id=self.kwargs.get('closetid'), closetUser=self.request.user)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def list(request):
    return render(request, 'main/list.html', {'title': 'list'})

@login_required
def myClosets(request):
    # Render the initial page
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
    username = request.user.username
    closet = get_object_or_404(Closet, id=closetid)
    clothes_in_closet = closetClothes.objects.filter(closet=closet)
    empty = not clothes_in_closet.exists()
    
    # Organize clothes by category without using defaultdict
    categorized_clothes = {}
    for closet_item in clothes_in_closet:
        category = closet_item.clothing_item.category.category
        if category not in categorized_clothes:
            categorized_clothes[category] = [closet_item.clothing_item]
        else:
            categorized_clothes[category].append(closet_item.clothing_item)

    outfits = [o.outfit for o in closetOutfits.objects.filter(closet=closet)]
    
    context = {
        'closet': closet,
        'username': username,
        'categorized_clothes': categorized_clothes,
        'title': closet.name,
        'empty': empty,
        'user_outfits': outfits
    }

    return render(request, 'blog/open_my_closet.html', context)

@login_required
def openUserCloset(request, username=None, closetname=None):
    user = User.objects.get(username=username)
    closet = get_object_or_404(Closet, name=closetname, closetUser=user)
    clothes_in_closet = closetClothes.objects.filter(closet=closet)
    empty = not clothes_in_closet.exists()
    
    # Organize clothes by category without using defaultdict
    categorized_clothes = {}
    for closet_item in clothes_in_closet:
        category = closet_item.clothing_item.category.category
        if category not in categorized_clothes:
            categorized_clothes[category] = [closet_item.clothing_item]
        else:
            categorized_clothes[category].append(closet_item.clothing_item)

    outfits = [o.outfit for o in closetOutfits.objects.filter(closet=closet)]
    
    context = {
        'closet': closet,
        'username': username,
        'categorized_clothes': categorized_clothes,
        'title': closet.name,
        'empty': empty,
        'user_outfits': outfits
    }

    return render(request, 'blog/open_user_closet.html', context)

@login_required
def Clothes(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        user_clothes = userClothes.objects.filter(bloguser=request.user)
        categories = clothingCategories.objects.values_list('category', flat=True).distinct()
        styles = clothingStyles.objects.values_list('style', flat=True).distinct()
        color_list = colors.objects.values_list('color', flat=True).distinct()

        # Filtering logic
        category_filter = request.GET.get('category')
        style_filter = request.GET.get('style')
        color_filter = request.GET.get('color')

        filtered_items = user_clothes
        if category_filter:
            filtered_items = filtered_items.filter(category__category=category_filter)
        if style_filter:
            filtered_items = filtered_items.filter(style__style=style_filter)
        if color_filter:
            filtered_items = filtered_items.filter(color__color=color_filter)

        context = {
            'user': request.user,
            'username': username,
            'userClothes': user_clothes,
            'categories': categories,
            'styles': styles,
            'colors': color_list,  # Changed variable name to color_list
            'filteredItems': filtered_items,
            'empty': len(user_clothes) == 0
        }

        return render(request, 'blog/user_clothes.html', context)

@login_required
def createOutfit(request, closetid=None):
    # Ensure a valid closet is provided
    if closetid is not None:
        closet = get_object_or_404(Closet, id=closetid, closetUser=request.user)
    else:
        messages.error(request, "No valid closet specified.")
        return redirect('some-default-url')  # Redirect to a default URL

    if request.method == 'POST':
        # Extract item IDs from POST data
        top_id = request.POST.get('top')
        bottoms_id = request.POST.get('bottoms')
        footwear_id = request.POST.get('footwear')
        accessory_id = request.POST.get('accessory')  # These are optional, so they might be empty strings.
        outerwear_id = request.POST.get('outerwear')

        # Attempt to retrieve the corresponding userClothes instances
        try:
            top = userClothes.objects.get(id=top_id, bloguser=request.user, closetclothes__closet=closet) if top_id else None
            bottoms = userClothes.objects.get(id=bottoms_id, bloguser=request.user, closetclothes__closet=closet) if bottoms_id else None
            footwear = userClothes.objects.get(id=footwear_id, bloguser=request.user, closetclothes__closet=closet) if footwear_id else None
            accessory = userClothes.objects.get(id=accessory_id, bloguser=request.user, closetclothes__closet=closet) if accessory_id else None
            outerwear = userClothes.objects.get(id=outerwear_id, bloguser=request.user, closetclothes__closet=closet) if outerwear_id else None

            if not all([top, bottoms, footwear]):  # Make sure the required items are selected
                raise ValueError("Top, bottoms, and footwear are required to create an outfit.")

            outfit = Outfit(user=request.user, top=top, bottoms=bottoms, footwear=footwear, accessory=accessory, outerwear=outerwear)
            outfit.save()
            closetOutfit = closetOutfits(closet=closet, outfit=outfit, user=request.user)
            closetOutfit.save()

            messages.success(request, "Outfit created successfully!")
            return redirect(reverse('open-closet', kwargs={'closetid': closetid}))

        except userClothes.DoesNotExist:
            messages.error(request, "One or more selected items were not found.")
        except ValueError as e:
            messages.error(request, str(e))

    # If not POST method or if there was an error, re-display the form.
    categories = {
        'top': userClothes.objects.filter(category__category='Top', bloguser=request.user, closetclothes__closet=closet),
        'bottoms': userClothes.objects.filter(category__category='Bottoms', bloguser=request.user, closetclothes__closet=closet),
        'footwear': userClothes.objects.filter(category__category='Footwear', bloguser=request.user, closetclothes__closet=closet),
        'accessories': userClothes.objects.filter(category__category='Accessory', bloguser=request.user, closetclothes__closet=closet),
        'outerwear': userClothes.objects.filter(category__category='Outerwear', bloguser=request.user, closetclothes__closet=closet)
    }

    return render(request, 'blog/create_outfit.html', {'categories': categories, 'closet': closet})



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

@login_required
def deleteOutfit(request, closetid=None, outfitid=None):
    coutfit = get_object_or_404(closetOutfits, closet=closetid, outfit=outfitid)
    outfit = coutfit.outfit
    coutfit.delete()
    outfit.delete()
    return redirect(reverse('open-closet', kwargs={'closetid': closetid}))

class SearchView(ListView):
    model = User
    template_name = "blog/user_list.html"
    context_object_name = 'users'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(username__icontains=search_query)
        return queryset

@login_required
def view_outfits(request):
    user_outfits = Outfit.objects.filter(user=request.user)  # Get all outfits for the logged-in user
    return render(request, 'blog/view_outfits.html', {'user_outfits': user_outfits})

@login_required
def new_message(request, user_pk):
    recipient = get_object_or_404(User, pk=user_pk)
    if recipient == request.user:
        return redirect('blog/why.html')  # Redirect to prevent messaging oneself.

    # Check if there is an existing conversation between the users
    existing_convos = Convo.objects.filter(members=request.user).filter(members=recipient).distinct()
    if existing_convos.exists():
        return redirect('view-message', pk=existing_convos.first().id)  # Use the appropriate path name

    if request.method == 'POST':
        form = DirectMessagingForm(request.POST)
        if form.is_valid():
            convo = Convo.objects.create()  # No need to attach user directly to Convo
            convo.members.add(request.user, recipient)
            convo_message = form.save(commit=False)
            convo_message.conversing = convo
            convo_message.created_by = request.user
            convo_message.save()
            return redirect('view-message', pk=convo.id)  # Ensure this redirect is correct
    else:
        form = DirectMessagingForm()

    return render(request, 'blog/new.html', {'form': form, 'recipient': recipient})  # Adjust template path if needed

@login_required
def dm(request):
     convos = Convo.objects.filter(members__in=[request.user.id])

     return render(request, 'blog/dm.html',{
         'convos': convos,
     })

@login_required
def detailM(request, pk):
    convo = Convo.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form = DirectMessagingForm(request.POST)
        if form.is_valid():
            convo_message = form.save(commit=False)
            convo_message.conversing = convo
            convo_message.created_by = request.user
            convo_message.save()

            convo.save()
            return redirect('view-message',pk=pk)
    else:
        form = DirectMessagingForm()
        

    return render(request, 'blog/detailM.html', {
        'convo': convo,
        'form': form
    })
    
def why(request):
    return render(request, 'blog/why.html')