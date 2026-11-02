from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from .models import Post


class IndexView(TemplateView):
    template_name = "blog/index.html"


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 2

class PostDetailView(DetailView):
    model = Post
