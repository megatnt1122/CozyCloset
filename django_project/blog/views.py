from django.shortcuts import render, get_object_or_404, redirect, reverse
import random
from collections import defaultdict
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import View
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
from collections import defaultdict

@login_required
def LikeView(request, pk):
    post = get_object_or_404(Post, id=pk)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    total_likes = post.likes.count()
    
    return JsonResponse({'liked': liked, 'total_likes': total_likes})

@login_required
def CommentLikeView(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    liked = False
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True

    total_likes = comment.likes.count()
    return JsonResponse({'liked': liked, 'total_likes': total_likes})


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    login_url = reverse_lazy('login')  # Specify the login URL

    def get_queryset(self):
        # Get the IDs of followed users
        followed_user_ids = Follow.objects.filter(follower=self.request.user).values_list('followed_id', flat=True)
        # Fetch posts from followed users
        followed_user_posts = super().get_queryset().filter(author_id__in=followed_user_ids)
        return followed_user_posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all comments related to the posts fetched in the queryset
        post_ids = [post.id for post in context['posts']]
        comments = Comment.objects.filter(post_id__in=post_ids)
        context['comments'] = comments
        allposts = Post.objects.exclude(id__in=post_ids)
        context['allposts'] = allposts
        return context


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
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = post.total_likes()
        comments = Comment.objects.filter(post=post)
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        context["total_likes"] = total_likes
        context["liked"] = liked
        context["comments"] = comments
        return context

class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/add_comment.html'  # Adjust if needed

    def form_valid(self, form):
        # Set the post reference on the new comment instance
        form.instance.post_id = self.kwargs['pk']
        # Attach the logged-in user as the commenter
        form.instance.name = self.request.user.username
        # Save the form instance but do not redirect
        self.object = form.save()

        # Check if the request is an AJAX request
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = {
                'success': True,
                'comment_id': self.object.id,
                'name': self.object.name.username,  # Assuming you have a username field in your User model
                'date_added': self.object.date_added.strftime("%m/%d/%Y, %H:%M"),  # Format the date however you like
                'body': self.object.body,
            }
            return JsonResponse(data)
        else:
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddCommentView, self).get_context_data(**kwargs)
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        context['post'] = post
        context['comments'] = post.comments.all()  # Assuming a reverse relationship from Post to Comment
        return context

@login_required
def deleteComment(request, commentid=None):
    comment = get_object_or_404(Comment, id=commentid)
    comment.delete()
    return JsonResponse({'message': 'Comment deleted successfully'})

@login_required
def createPost(request, itemid=None):
    try:
        shareditem = userClothes.objects.get(id=itemid)
    except userClothes.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
        else:
            raise Http404("Item not found")

    form = PostForm(request.POST or None, request.FILES or None, shareditem=shareditem)

    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if shareditem:
                post.image = shareditem.image  # Use image from shared item
            post.save()
            # Redirect on successful submission
            return redirect(post.get_absolute_url())
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return only the necessary HTML for the AJAX-loaded modal
        return render(request, 'blog/post_form.html', {'form': form, 'shareditem': shareditem})
    else:
        # Return the full page if not an AJAX request
        return render(request, 'blog/post_form.html', {'form': form, 'shareditem': shareditem})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content']

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

@login_required
def userProfile(request, username):
    user = get_object_or_404(User, username=username)
    
    followerscount = Follow.objects.filter(followed=user).count()
    followingcount = Follow.objects.filter(follower=user).count()
    status = Follow.objects.filter(follower=request.user, followed=user).exists()

    # Define the UserPostListView class
    class UserPostListView(ListView):
        model = Post
        template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
        context_object_name = 'posts'
        paginate_by = 5

        def get_queryset(self):
            # Retrieve posts by the specified user
            return Post.objects.filter(author=user).order_by('-date_posted')

    # Create an instance of the UserPostListView
    post_list_view = UserPostListView()
    post_list_view.request = request  # Set the request attribute
    post_form = PostForm()

    # Render the template with the context
    context = {
        'user': user,
        'followerscount': followerscount,
        'followingcount': followingcount,
        'status': status,
        'closets': Closet.objects.filter(closetUser=user),
        'posts': Post.objects.filter(author=user).order_by('-date_posted'),
        'post_list': post_list_view,  # Pass the post_list_view instance to the template
        'form': post_form
    }

    return render(request, 'blog/user_profile.html', context)


# the view for the upload page
class UploadView(LoginRequiredMixin, CreateView):
    model = userClothes
    fields = ['name','category','style','color','image']
    success_url = reverse_lazy('upload')

    def form_valid(self, form):
        form.instance.bloguser = self.request.user 
        response = super().form_valid(form)  
        messages.success(self.request, 'Your item was uploaded successfully!')
        return response

# the view for creating a new closet
class ClosetCreateView(LoginRequiredMixin, CreateView):
    model = Closet
    fields = ['name', 'is_public']

    # links the current user to the closet being created
    def form_valid(self, form):
        form.instance.closetUser = self.request.user
        return super().form_valid(form)

class ClosetUpdateView(LoginRequiredMixin, UpdateView):
    model = Closet
    fields = ['name', 'is_public']
    template_name = 'blog/closet_edit.html'

    def get_success_url(self):
        return reverse('my-closets')

    def get_object(self):
        return get_object_or_404(Closet, id=self.kwargs.get('closetid'), closetUser=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'redirect_url': self.get_success_url()})
        else:
            return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(form.errors, status=400)
        else:
            return response


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
    create_outfits = True
    closet = get_object_or_404(Closet, id=closetid)
    clothes_in_closet = closetClothes.objects.filter(closet=closet)
    empty = not clothes_in_closet.exists()
    
    # Define a mapping from specific categories to general categories
    category_mapping = {
        'Long Sleeve': 'Tops',
        'Short Sleeve': 'Tops',
        'Pants': 'Bottoms',
        'Shorts': 'Bottoms',
        'Footwear': 'Footwear',
        'Outerwear': 'Outerwear',
        'Accessories': 'Accessories',
    }
    
    # Organize clothes by general categories using the mapping
    categorized_clothes = {}
    for closet_item in clothes_in_closet:
        specific_category = closet_item.clothing_item.category.category
        general_category = category_mapping.get(specific_category, specific_category)  # Default to specific if not mapped
        if general_category not in categorized_clothes:
            categorized_clothes[general_category] = [closet_item.clothing_item]
        else:
            categorized_clothes[general_category].append(closet_item.clothing_item)

    # Define category order
    category_order = ['Tops', 'Bottoms', 'Footwear', 'Outerwear', 'Accessories']

    # Sort the categories based on the predefined order
    sorted_categorized_clothes = {category: categorized_clothes[category] for category in category_order if category in categorized_clothes}

    outfits = [o.outfit for o in closetOutfits.objects.filter(closet=closet)]

    # Check if there is at least one top, bottom, and footwear item
    has_top = 'Tops' in sorted_categorized_clothes and len(sorted_categorized_clothes['Tops']) > 0
    has_bottom = 'Bottoms' in sorted_categorized_clothes and len(sorted_categorized_clothes['Bottoms']) > 0
    has_footwear = 'Footwear' in sorted_categorized_clothes and len(sorted_categorized_clothes['Footwear']) > 0

    if not has_top or not has_bottom or not has_footwear:
        create_outfits = False
    
    context = {
        'closet': closet,
        'username': username,
        'categorized_clothes': sorted_categorized_clothes,
        'title': closet.name,
        'empty': empty,
        'user_outfits': outfits,
        'closetId': closetid,
        'create_outfits': create_outfits
    }

    return render(request, 'blog/open_my_closet.html', context)

@login_required
def openUserCloset(request, username=None, closetname=None):
    user = User.objects.get(username=username)
    closet = get_object_or_404(Closet, name=closetname, closetUser=user)
    clothes_in_closet = closetClothes.objects.filter(closet=closet)
    empty = not clothes_in_closet.exists()

    # Define a mapping from specific categories to general categories
    category_mapping = {
        'Long Sleeve': 'Tops',
        'Short Sleeve': 'Tops',
        'Pants': 'Bottoms',
        'Shorts': 'Bottoms',
        'Footwear': 'Footwear',
        'Outerwear': 'Outerwear',
        'Accessories': 'Accessories',
    }
    
    # Organize clothes by general categories using the mapping
    categorized_clothes = {}
    for closet_item in clothes_in_closet:
        specific_category = closet_item.clothing_item.category.category
        general_category = category_mapping.get(specific_category, specific_category)  # Default to specific if not mapped
        if general_category not in categorized_clothes:
            categorized_clothes[general_category] = [closet_item.clothing_item]
        else:
            categorized_clothes[general_category].append(closet_item.clothing_item)

    # Define category order
    category_order = ['Tops', 'Bottoms', 'Footwear', 'Outerwear', 'Accessories']

    # Sort the categories based on the predefined order
    sorted_categorized_clothes = {category: categorized_clothes[category] for category in category_order if category in categorized_clothes}

    outfits = [o.outfit for o in closetOutfits.objects.filter(closet=closet)]
    
    context = {
        'closet': closet,
        'username': username,
        'categorized_clothes': sorted_categorized_clothes,
        'title': closet.name,
        'empty': empty,
        'user_outfits': outfits,
        'closetId': closet.id
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
        top_id = request.POST.get('selectedTop')
        bottoms_id = request.POST.get('selectedBottoms')
        footwear_id = request.POST.get('selectedFootwear')
        accessory_id = request.POST.get('selectedAccessory') 
        outerwear_id = request.POST.get('selectedOuterwear')

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

            messages.success(request, ' ')
            return redirect(reverse('open-closet', kwargs={'closetid': closetid}))

        except userClothes.DoesNotExist:
            messages.error(request, "One or more selected items were not found.")
        except ValueError as e:
            messages.error(request, str(e))

    # If not POST method or if there was an error, re-display the form.
    categories = {
        'top': userClothes.objects.filter(
            Q(category__category='Long Sleeve') | Q(category__category='Short Sleeve'), 
            bloguser=request.user, 
            closetclothes__closet=closet
        ),
        'bottoms': userClothes.objects.filter(
            Q(category__category='Pants') | Q(category__category='Shorts'), 
            bloguser=request.user, 
            closetclothes__closet=closet
        ),
        'footwear': userClothes.objects.filter(
            category__category='Footwear', 
            bloguser=request.user, 
            closetclothes__closet=closet
        ),
        'accessory': userClothes.objects.filter(
            category__category='Accessory', 
            bloguser=request.user, 
            closetclothes__closet=closet
        ),
        'outerwear': userClothes.objects.filter(
            category__category='Outerwear', 
            bloguser=request.user, 
            closetclothes__closet=closet
        )
    }

    

    return render(request, 'blog/create_outfit.html', {
        'categories': categories,
        'closet': closet
    })


@login_required
def AddToCloset(request, itemid=None):
    item = userClothes.objects.get(id=itemid)

    if request.method == 'POST':
        closets_ids = [key.split('_')[1] for key in request.POST.keys() if key.startswith('closet_')]
        for closet_id in closets_ids:
            closet = Closet.objects.get(id=closet_id)
            adding = closetClothes(closet=closet, clothing_item=item, user=request.user)
            adding.save()

        return redirect('my-clothes')

    closets = Closet.objects.filter(closetUser=request.user).exclude(closetclothes__clothing_item=item)

    context = {
        'user': request.user,
        'closets': closets,
        'item': item
    }

    return render(request, 'blog/AddToCloset.html', context)

@login_required
def deleteItem(request, itemid=None, closetid=None):
    # get item from database
    item = get_object_or_404(userClothes, id=itemid)
    if closetid is None:
        # delete item
        item.delete()
        return JsonResponse({'message': 'Item deleted successfully'})
    else:
        closet = get_object_or_404(Closet, id=closetid)
        closetitem = get_object_or_404(closetClothes, closet=closet, clothing_item=item)
        closetitem.delete()
        return JsonResponse({'message': 'Item deleted successfully'})

@login_required
def deleteCloset(request, closetid=None):
    closet = get_object_or_404(Closet, id=closetid)
    closet.delete()
    return redirect(reverse('my-closets'))

@login_required
def deleteOutfit(request, outfitid=None):
    coutfit = get_object_or_404(closetOutfits, outfit=outfitid, user=request.user)
    outfit = coutfit.outfit
    coutfit.delete()
    outfit.delete()
    return JsonResponse({'status': 'success', 'message': 'Outfit deleted'})

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = context['users']
        current_user = self.request.user
        users = [user for user in users if user != current_user]
        following_status = {}
        follows = Follow.objects.filter(follower=current_user, followed__in=users)
        for user in users:
            following_status[user] = follows.filter(followed=user).exists()
        context['following_status'] = following_status
        return context

@login_required
def view_outfits(request):
    user_outfits = Outfit.objects.filter(user=request.user)  # Get all outfits for the logged-in user
    return render(request, 'blog/view_outfits.html', {'user_outfits': user_outfits})

@login_required
def new_message(request, user_pk):
    recipient = get_object_or_404(User, pk=user_pk)
    if recipient == request.user:
        return redirect('blog-home')  # Redirect to prevent messaging oneself.

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
            convo.last_message = convo_message.content
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
    
    # Find the other user in the convo
    recipient = convo.members.exclude(id=request.user.id).first()

    if request.method == 'POST':
        form = DirectMessagingForm(request.POST)
        if form.is_valid():
            convo_message = form.save(commit=False)
            convo_message.conversing = convo
            convo_message.created_by = request.user
            convo_message.save()
            convo.last_message = convo_message.content
            convo.save()
            return redirect('view-message', pk=pk)
    else:
        form = DirectMessagingForm()

    return render(request, 'blog/detailM.html', {
        'convo': convo,
        'form': form,
        'recipient': recipient  # Adding recipient to the context
    })

    
@method_decorator(login_required, name='dispatch')
class FollowUserView(View):
    def post(self, request, username):
        user_to_follow = get_object_or_404(User, username=username)
        follow, created = Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
        if created:
            # Optionally send a notification to `user_to_follow`, or do any other additional actions
            pass
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@method_decorator(login_required, name='dispatch')
class UnfollowUserView(View):
    def post(self, request, username):
        user_to_unfollow = get_object_or_404(User, username=username)
        try:
            follow = Follow.objects.get(follower=request.user, followed=user_to_unfollow)
            follow.delete()
            # Optionally add some kind of notification that they've unfollowed
        except Follow.DoesNotExist:
            pass
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
