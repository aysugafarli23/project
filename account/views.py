# myapp/views.py
from django.shortcuts import render
from .forms import Nativel
    
def nativel(request):
    if request.method == 'POST':
        form = Nativel(request.POST or None)
        if form.is_valid():
            # Process form data here (e.g., save to database)
            pass
    else:
        form = Nativel()
    context = {"form": form}
    return render(request, 'nativel.html', context)
