from django.shortcuts import render


def TFIDFManual(request):
    title = 'This is a variable'

    return render(request, 'TF_IDF/manual.html', {'title': title})



def TFIDFLib(request):
    title = 'This is a variable'

    return render(request, 'TF_IDF/lib.html', {'title': title})