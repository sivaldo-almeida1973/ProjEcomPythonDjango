from django.shortcuts import render

# Create your views here. 4º passo
def homepage(request):
  return render(request, 'homepage.html')