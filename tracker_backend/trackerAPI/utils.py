from django.shortcuts import render


# Project link to API documentation
def documentation(request):
    return render(request, 'documentation.html')
