from django.shortcuts import render


def pageRankManual(request):
    title = 'This is a variable'

    return render(request, 'TF_IDF/manual.html', {'title': title})



def pageRankLib(request):
    title = 'This is a variable'

    return render(request, 'TF_IDF/lib.html', {'title': title})