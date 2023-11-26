from django.shortcuts import render


# Create your views here.
def manual(request):
    return render(request, 'page_rank/manual.html')


def lib(request):
    return render(request, 'page_rank/lib.html')
