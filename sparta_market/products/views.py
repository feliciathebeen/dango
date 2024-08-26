from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST

from .models import Article
from .forms import ArticleForm


def home(request):
    articles = Article.objects.all().order_by("-id")
    context = {
        "articles": articles,
    }
    return render(request, "products/home.html", context)


def detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        "article": article,
    }
    return render(request, "products/detail.html", context)


@login_required
def create(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES.get('image')

        article = Article.objects.create(
            author = request.user,
            title = title,
            content = content,
            image = image
        )

        return redirect('products:detail', pk=article.pk)
    
    return render(request, 'products/create.html')


@login_required
@require_http_methods(["GET", "POST"])
def update(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.author == request.user:
        if request.method == "POST":
            form = ArticleForm(request.POST, request.FILES, instance=article)
            if form.is_valid():
                article = form.save()
                return redirect("products:detail", article.pk)
        else:
            form = ArticleForm(instance=article)
    else:
        return redirect("products:home")
    
    context = {
        "form": form,
        "article": article,
    }
    
    return render(request, "products/update.html", context)


@require_POST
def delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user.is_authenticated:
        if article.author == request.user:
            article = get_object_or_404(Article, pk=pk)
            article.delete()
    return redirect("products:home")