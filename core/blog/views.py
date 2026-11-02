from django.views.generic.base import TemplateView
from django.views.generic import ListView
from .models import Post


class IndexView(TemplateView):
    template_name = "blog/index.html"


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
