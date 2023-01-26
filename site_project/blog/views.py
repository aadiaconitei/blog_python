from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy, reverse
from .models import Post, Category, Comment
from .forms import AddCommentForm


def homepage(request):
    categories = Category.objects.all()
    # featured = Post.objects.filter(status=1)
    latest = Post.objects.filter(status=1).order_by('-post_date')[0:3]
    context = {
        # 'object_list': featured,
        'latest': latest,
        'categories': categories,
    }
    return render(request, 'homepage.html', context)


def posts(request):
    categories = Category.objects.all()
    featured = Post.objects.filter(status=1)
    paginator = Paginator(featured, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'object_list': page_obj,
        'categories': categories,
    }
    return render(request, 'posts.html', context)


def post(request, pk):
    categories = Category.objects.all()
    post = Post.objects.get(id=pk)
    total_likes = post.total_likes()
    liked = False
    context = {
        'post': post,
        'total_likes': total_likes,
        'liked': liked,
        'categories': categories,
    }
    return render(request, 'post_details.html', context)


def category_view(request, category):
    category_posts = Post.objects.filter(category_id=category)
    categories = Category.objects.all()
    cats = Category.objects.get(id=category)
    print(cats)
    context = {
        'category_posts': category_posts,
        'category': category,
        'category_name': cats,
        'categories': categories,
        'active': 1
    }
    return render(request, 'filter_by_categories.html', context)


def like_view(request, pk):
    try:
        post_obj = get_object_or_404(Post, id=request.POST['post_id'])
        liked = False
        if post_obj.likes.filter(id=request.user.id).exists():
            post_obj.likes.remove(request.user)
            liked = False
        else:
            post_obj.likes.add(request.user)
            liked = True

        return HttpResponseRedirect(reverse('post', args=[str(pk)]))

    except Post.DoesNotExist:
        raise Http404("Eroare 404.")


class AddCommentView(CreateView):
    model = Comment
    form_class = AddCommentForm
    template_name = 'add_comment.html'

    def get_success_url(self):
        post_id = self.kwargs['pk']
        return reverse_lazy('post', kwargs={'pk': post_id})  # return to article.
        # return reverse_lazy('homepage')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)


class SearchResultsView(ListView):
    model = Post
    template_name = 'search_results.html'
    cats = Category.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        search = self.request.GET.get('search')
        # context['data'] = Post.objects.filter(title=search)
        # context['data'] = Post.objects.filter(title__contains=search)
        context['data'] = Post.objects.filter(title__icontains=search)
        context['search'] = search

        return context


