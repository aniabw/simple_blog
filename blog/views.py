from django.shortcuts import redirect
from django.views import generic

from django.views.generic.edit import FormMixin
from .forms import CommentForm
from .models import Post


class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 5
    model = Post

    def get_queryset(self):
        return Post.objects.order_by('-created_at')


class DetailView(FormMixin, generic.DetailView):
    model = Post
    template_name = 'blog/detail.html'

    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.save()
            return redirect('detail', company_id=self.object.company_id)
        else:
            return self.form_invalid(form)