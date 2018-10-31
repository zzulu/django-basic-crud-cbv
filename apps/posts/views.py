from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment
from .forms import CommentForm


class PostList(generic.ListView):
    # Set tamplate name. Default is 'posts/post_list.html'.
    # All classes below this class have their default template name.
    # template_name = 'posts/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all()


class PostCreate(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['content',]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostDetail(generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'post': self.object})
        return context


class PostUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ['content',]

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user != self.request.user:
            return HttpResponseForbidden("You are not allowed to edit this Post")
        return super().dispatch(request, *args, **kwargs)


class PostDelete(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('posts:list')

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user != self.request.user:
            return HttpResponseForbidden("You are not allowed to delete this Post")
        return super().dispatch(request, *args, **kwargs)


class CommentCreate(LoginRequiredMixin, generic.CreateView):
    model = Comment
    fields = ['content',]
    http_method_names = ['post',]
 
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        return super().form_valid(form)


class CommentDelete(LoginRequiredMixin, generic.DeleteView):
    http_method_names = ['post',]
    model = Comment

    def get_success_url(self):
        return reverse('posts:detail', kwargs={'pk': self.object.post_id})

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user != self.request.user:
            return HttpResponseForbidden("You are not allowed to delete this Comment")
        return super().dispatch(request, *args, **kwargs)
