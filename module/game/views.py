from django.shortcuts import render
from .models import MatchingGameWord, Score
import random

# Create your views here.
def match_voice(request):
    words = MatchingGameWord.objects.order_by('?')[:12]
    words2 = list(words)
    random.shuffle(words2)

    return render(request, 'matchvoice.html', {'words1': words, 'words2': words2})


def gameover(request):
    best_user_score = Score.objects.filter(user=request.user).order_by('seconds').first()
    top_5_scores = Score.objects.order_by('seconds')[:5]
    
    if request.method == 'POST':
        new_score = request.POST.get('new_score')
        if new_score:
            score_record = Score.objects.create(user=request.user, seconds=new_score)
            score_record.save()
    
    context = {
        'best_user_score': best_user_score,
        'top_5_scores': top_5_scores,
    }
    return render(request, 'gameover.html', context)