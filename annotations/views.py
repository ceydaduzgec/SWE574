from django.shortcuts import render
from .models import WebAnnotation
from .forms import WebAnnotationForm

def web_annotations_list(request):
    annotations = WebAnnotation.objects.all()
    if request.method == 'POST':
        form = WebAnnotationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = WebAnnotationForm()
    return render(request, 'webannotations/list.html', {'annotations': annotations, 'form': form})
# Create your views here.
