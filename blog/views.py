from django.shortcuts import render

def main(request):
    return render(request, 'blog/index.html', {})
