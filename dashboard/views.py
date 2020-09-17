from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib.auth.models import User
from comment.models import Comment

from .models import Book
from .forms import BookForm
from itertools import chain
from comment.forms import CommentForm
from django.contrib import messages


class BookList(ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'book_list.html'
    paginate_by = 12


@method_decorator(login_required, name="dispatch")
class BookDetail(DeleteView):
    model = Book
    context_object_name = 'books'
    template_name = 'book_detail.html'


@login_required
def bookCreate(request):
    model = Book
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.created_at = timezone.now()
            book.created_by = request.user
            book.save()
            SuccessMessageMixin = "图书发布成功！"
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'book_new.html', {'form': form})


@method_decorator(login_required, name="dispatch")
class BookUpdate(SuccessMessageMixin, UpdateView):
    model = Book
    context_object_name = 'books'
    form_class = BookForm
    success_url = reverse_lazy('book_list')
    success_message = '信息更新成功！'
    template_name = 'book_update.html'


@method_decorator(login_required, name="dispatch")
class BookDelete(SuccessMessageMixin, DeleteView):
    model = Book
    context_object_name = 'books'
    success_url = reverse_lazy('book_list')
    success_message = "图书已删除！"
    template_name = 'book_delete.html'


class SearchView(ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'search.html'
    paginate_by = 12
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

        if query is not None:
            blog_results = Book.objects.search(query)

            queryset_chain = chain(
                blog_results,
            )
            qs = sorted(queryset_chain,
                        key=lambda instance: instance.pk,
                        reverse=True)
            self.count = len(qs)
            return qs
        return Book.objects.none()


def book_detail(request, pk):
    template_name = 'book_detail.html'
    book = get_object_or_404(Book, pk=pk)

    comments = book.comment_set.all()

    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        comment_form.instance.book = book
        reply_id = request.POST.get('comment_id')
        if reply_id:
            comment_qs = Comment.objects.get(id=reply_id)
            comment_form.instance.reply = comment_qs
        comment_form.instance.author = request.user
        if comment_form.is_valid():
            comment_form.save()
            messages.success(request, f'评论已提交，核审通过后展示。')
            return redirect(f'/detail/{pk}')

    else:
        comment_form = CommentForm()

    return render(request, template_name, {'books': book,
                                           'comments': comments,
                                           'comment_form': comment_form})


class UserBookListView(ListView):
    model = Book
    template_name = 'user_book_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Book.objects.filter(created_by=user).order_by('-created_at')


def about(request):
    return render(request, 'about.html')
