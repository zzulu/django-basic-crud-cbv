from django.shortcuts import render # Not used
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment
from .forms import CommentForm


class PostList(ListView):
    # Set tamplate name. Default is 'posts/post_list.html'.
    # All classes below this class have their default template name.
    # template_name = 'posts/index.html'
    model = Post
    context_object_name = 'posts'

    # Set query set. Same as model = Post.
    # def get_queryset(self):
    #     return Post.objects.all()


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content',]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PostCreate, self).form_valid(form)


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        # context['form'] = CommentForm(initial={'post': self.object})
        context['form'] = CommentForm()
        return context


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['content',]

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user != self.request.user:
            return HttpResponseForbidden("You are not allowed to edit this Post.")
        return super(PostUpdate, self).dispatch(request, *args, **kwargs)


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('posts:list')

    def delete(self, request, *args, **kwargs):
        if self.get_object().user != self.request.user:
            return HttpResponseForbidden("You are not allowed to delete this Post.")
        return super(PostDelete, self).delete(request, *args, **kwargs)


class CommentCreate(LoginRequiredMixin, CreateView):
    http_method_names = ['post',]
    model = Comment
    fields = ['content',]
 
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post_id = self.kwargs.get('post_id')
        return super(CommentCreate, self).form_valid(form)


class CommentDelete(LoginRequiredMixin, DeleteView):
    http_method_names = ['post',]
    model = Comment

    def get_success_url(self):
        return reverse('posts:detail', kwargs={'pk': self.kwargs.get('post_id')})

    def delete(self, request, *args, **kwargs):
        if self.get_object().user != self.request.user:
            return HttpResponseForbidden("You are not allowed to delete this Comment.")
        return super(CommentDelete, self).delete(request, *args, **kwargs)
