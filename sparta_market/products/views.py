from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST
from django.db.models import Count
from django.db.models import Q
from django.http import HttpResponseRedirect

from .models import Article, Comment, Hashtag
from .forms import ArticleForm, CommentForm


def home(request):
    sort_option = request.GET.get('sort', 'latest')

    if sort_option == 'popular':
        articles = Article.objects.annotate(like_count=Count('like_users')).order_by('-like_count', '-created_at')
    else:
        articles = Article.objects.order_by('-created_at')
    
    context = {
        'articles': articles, 
        'sort_option': sort_option,
    }

    return render(request, 'products/home.html', context)


def search(request) :
    word= request.GET.get('word')
    outcomes = Article.objects.filter( Q(title__icontains=word) | Q(content__icontains=word) | Q(author__username__icontains=word)  ).order_by('-id')

    context = {'word': word,
             'outcomes': outcomes, }
    return render(request, 'products/search.html', context )


def detail(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = article.comments.all()
    # 조회수 증가
    article.view_count += 1
    article.save()

    print(comments)
    context = {
        "article": article,
        "comment_form": comment_form,
        "comments": comments,
    }
    return render(request, "products/detail.html", context)


@login_required
def create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            # 최종 저장된 content를 조작하기 위해 article.save()보다 아래에 작성
            for word in article.content.split():  # content를 공백기준 리스트로 변경
                if word.startswith('#'):  # '#' 로 시작하는 요소 선택
                   hashtag, created = Hashtag.objects.get_or_create(content=word)
                   article.hashtags.add(hashtag)
            return redirect("products:detail", article.pk)
    else:
        form = ArticleForm()
    context = {"form": form}
    return render(request, "products/create.html", context)


@login_required
def hashtag(request, pk):
    hashtag = get_object_or_404(Hashtag, pk=pk)
    articles = hashtag.article_hashtag.order_by('-pk')
    context = {
        'hashtag': hashtag, 
        'articles': articles,
    }
    return render(request, 'products/hashtag.html', context)


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


@require_POST
def comment_create(request, pk):
    article = get_object_or_404(Article, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.user = request.user
        comment.save()
    return redirect("products:detail", article.pk)


@require_POST
def comment_delete(request, pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.user == request.user:
            comment.delete()
    return redirect("products:detail", pk)


@require_POST
def like(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=pk)
        if article.like_users.filter(pk=request.user.pk).exists():
            article.like_users.remove(request.user)
        else:
            article.like_users.add(request.user)
    else:
        return redirect("accounts:login")
    
    # 사용자가 디테일 페이지에 있었다면 디테일 페이지로 리디렉션
    if 'detail' in request.META.get('HTTP_REFERER', ''):
        return redirect("products:detail", pk=pk)

    # 그렇지 않으면 현재 페이지 유지
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    