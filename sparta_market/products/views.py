from django.shortcuts import render


def home(request):
    member = request.user
    context = {
        "member" : member
    }
    return render(request, "products/home.html", context)
