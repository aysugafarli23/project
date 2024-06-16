from django.shortcuts import render, redirect
from django.urls import resolve
from django.contrib import messages
from contact.forms import ContactForm  
from openai import OpenAI
from pathlib import Path

# Create your views here.

def modulesPage(request):
     # Contact form logic
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = ContactForm()
    current_url = resolve(request.path_info).url_name
    context = {
        'current_url': current_url,
        'form': form,
    }
    
    return render(request, 'module.html', context)



def generate_speech():
    client=OpenAI(api_key = "sk-proj-8tsKt51ax7c9AoOO3RYST3BlbkFJkVGybZPjPoHTxK1LZXIm")
    speech_file_path = Path(__file__).parent / "speech.mp3"
    speech_file_path = Path(__file__).parent / "speech2.mp3"

    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="alloy",
        input="I see skies of blue and clouds of white\nThe bright blessed days, the dark sacred nights\nAnd I think to myself\nWhat a wonderful world"
    ) as response:
        response.stream_to_file(speech_file_path)
        
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="echo",
        input="Okay guys we'll learn English"
    ) as response:
        response.stream_to_file(speech_file_path)
        
generate_speech()






#Still not applied for now
# def calculate_cost(text_string, model_id):
#     cost_tier = {
#         'tts-1': 0.015,
#         'tts-1-hd': 0.03
#     }
#     cost_unit = cost_tier.get(model_id, None)
#     if cost_unit is None:
#         return None
#     return (cost_unit * len(text_string)) / 1000
