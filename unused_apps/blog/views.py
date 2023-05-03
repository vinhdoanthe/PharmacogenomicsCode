from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView
# Create your views here.


def home(request):

    # for i in range(50):
    #     p = Post(title="title"+str(i), author="author"+str(i))
    #     p.save()
    context = {
        "posts": Post.objects.all()
    }

    return render(request, "blog/home.html", context)


class PostListView(ListView):
    context = {
        "posts": Post.objects.all()
    }
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    paginate_by = 7


class PostDetailView(DetailView):
    model = Post


def about(request):

    context = {}
    return render(request, "blog/about.html", context)
