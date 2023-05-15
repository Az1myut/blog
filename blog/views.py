
from django.contrib import messages
from django.core.signing import Signer
from blog.signals import my_signal
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from icecream import ic

from blog.forms import PostForm


from .models import Post
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin


class PostCreateView(SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_create.html"
    success_message = "Пост успешно создан"
    success_url = "/posts/add/"


class PostUpdateView(SuccessMessageMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_create.html"
    success_message = "Пост успешно сохранён"

    def get_success_url(self) -> str:
        return reverse_lazy("post_update", kwargs={"pk": self.kwargs["pk"]})


class PostsListView(ListView):
    model = Post
    template_name = "blog/posts_list.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs) -> dict:
        context = super(PostsListView, self).get_context_data(**kwargs)
        request = self.request

        if request.user.has_perm("blog.hide_comments"):
            context["hide_comments"] = "Mожно скрыть комментарии"
        else:
            context["hide_comments"] = "Нельзя скрыть комментарии"
        context["user"] = self.request.user
        
        # Call custom signal
        my_signal.send(sender=request.user, request=request, instance=context, created=False)
        return context

    
class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/signed_post.html'
    
    # def get_context_data(self, **kwargs):
    #     ic('yehuuu')
    #     context  =  super(PostDetailView, self).get_context_data(**kwargs)
    #     ic(kwargs)
    #     post = kwargs['object']
    #     signed_text = Signer().sign(post.text)
    #     context['signed_text'] = signed_text
    #     return context

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        signed_text = Signer().sign(post.text)
        ic(signed_text)
        signed_text = signed_text.split(':')[1]
        messages.add_message(request, settings.BAD_MESSAGE_TAG, signed_text)
        return render(request, template_name=self.template_name,context={})

        
        


