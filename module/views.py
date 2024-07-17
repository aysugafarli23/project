from django.shortcuts import render, redirect, get_object_or_404
from django.urls import resolve
from django.contrib import messages
from contact.forms import ContactForm  
from openai import OpenAI
from pathlib import Path
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
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
    
    modules = Module.objects.all()
    context = {
        'current_url': current_url,
        'form': form,
        'modules': modules,
    }
    return render(request, 'module.html', context)


def lessonsPage(request, pk):
    module = get_object_or_404(Module, pk=pk)
    lessons = Lesson.objects.filter(lesson_module=module)
    
    context = {
        'module': module,
        'lessons': lessons,        
    }
    
    return render(request, 'lesson.html', context)


def lessonSectionPage(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    sections = Section.objects.filter(section_lesson=lesson)
    section_contents = []

    for section in sections:
        section_contents.append({
            'section': section,
            'contents': Content.objects.filter(content_section=section)
        })

    context = {
        'lesson': lesson,
        'section_contents': section_contents,
    }
    return render(request, 'modulesections.html', context)


# def generate_speech():
#     client=OpenAI(api_key = "sk-proj-8tsKt51ax7c9AoOO3RYST3BlbkFJkVGybZPjPoHTxK1LZXIm")
#     speech_file_path = Path(__file__).parent / "speech.mp3"
#     speech_file_path = Path(__file__).parent / "speech2.mp3"

#     with client.audio.speech.with_streaming_response.create(
#         model="tts-1",
#         voice="alloy",
#         input="I see skies of blue and clouds of white\nThe bright blessed days, the dark sacred nights\nAnd I think to myself\nWhat a wonderful world"
#     ) as response:
#         response.stream_to_file(speech_file_path)
        
#     with client.audio.speech.with_streaming_response.create(
#         model="tts-1",
#         voice="echo",
#         input="Okay guys we'll learn English"
#     ) as response:
#         response.stream_to_file(speech_file_path)
        
# generate_speech()

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



def record_audio(request):
    return render(request, 'record_audio.html')

@csrf_exempt
# @login_required
def upload_media(request):
    if request.method == 'POST':
        if 'media' not in request.FILES:
            return JsonResponse({'success': False, 'error': 'No media file found'}, status=400)
        
        media_file = request.FILES['media']
        content_type = media_file.content_type
        content = Content.objects.create(
            title='Recorded Media',
            body='This is a recorded media file.',
            image=None,  # Assuming no image
            audio=media_file if content_type.startswith('audio/') else None,
            video=media_file if content_type.startswith('video/') else None
        )
        return JsonResponse({'success': True, 'content_id': content.id})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
    
 