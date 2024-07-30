from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import resolve
from contact.forms import ContactForm  
from pathlib import Path
from .models import *
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import Word, CustomerRecording
from openai import Client
from django.core.files import File
import re, os, tempfile
from django.views import View
from django.utils.decorators import method_decorator
from openai import OpenAI
from io import BytesIO
import numpy as np
from scipy.io import wavfile
import json
import pyaudio
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import random
import speech_recognition as sr
import openai
import time

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
    
    # Initializing section_contents
    section_contents = []
    
    for lesson in lessons:
        sections = Section.objects.filter(section_lesson=lesson)
        
        for section in sections:
            section_contents.append({
                'lesson': lesson,
                'section': section,
                'contents': Content.objects.filter(content_section=section)
            })

    context = {
        'module': module,
        'lessons': lessons,
        'section_contents': section_contents,
    }


    return render(request, 'lesson.html', context)


# a view to generate the audio files for each word using OpenAI
def generate_speech(request):
    words = Word.objects.all()
    client = Client(api_key="sk-proj-8tsKt51ax7c9AoOO3RYST3BlbkFJkVGybZPjPoHTxK1LZXIm")
    for word in words:
        filename = re.sub(r'[^\w\s-]', '', word.text)[:20].replace(' ', '_')  # Replace invalid characters with underscores
        speech_file_path = Path(__file__).parent / f"words_audio/{filename}_alloy.mp3"  # Add word ID to filename to avoid overwrites

        with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="alloy",
            input=word.text
        ) as response:
            response.stream_to_file(str(speech_file_path))  # Stream to the file path

        with open(speech_file_path, 'rb') as f:
            word.audio_file_alloy.save(speech_file_path.name, File(f), save=True)

    for word in words:
        filename = re.sub(r'[^\w\s-]', '', word.text)[:20].replace(' ', '_')  # Replace invalid characters with underscores
        speech_file_path = Path(__file__).parent / f"words_audio/{filename}_nova.mp3"  # Add word ID to filename to avoid overwrites

        with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="nova",
            input=word.text
        ) as response:
            response.stream_to_file(str(speech_file_path))  # Stream to the file path

        with open(speech_file_path, 'rb') as f:
            word.audio_file_nova.save(speech_file_path.name, File(f), save=True)


    return render(request, 'words.html', {'words': words})


@method_decorator(csrf_exempt, name='dispatch')
class WordView(View):
    template_name = 'word_detail.html'

    def get(self, request, word_id):
        word = get_object_or_404(Word, id=word_id)
        next_word = Word.objects.filter(id__gt=word_id).order_by('id').first()
        previous_word = Word.objects.filter(id__lt=word_id).order_by('-id').first()
        next_word_id = next_word.id if next_word else None
        previous_word_id = previous_word.id if previous_word else None
        return render(request, self.template_name, {
            'word': word,
            'next_word_id': next_word_id,
            'previous_word_id': previous_word_id
        })



    def post(self, request, word_id):
        word = get_object_or_404(Word, id=word_id)
        if 'media' in request.FILES:
            # Delete the previous recording
            CustomerRecording.objects.filter(word=word).delete()

            # Save the new recording
            media_file = request.FILES['media']
            customer_recording = CustomerRecording.objects.create(
                audio_file=media_file,
                word=word
            )
            return JsonResponse({'success': True, 'recording_id': customer_recording.id})
        return JsonResponse({'success': False, 'error': 'No media file found'}, status=400)

def compare_audio(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    recordings = CustomerRecording.objects.filter(word=word)
    next_word = Word.objects.filter(id__gt=word_id).order_by('id').first()
    next_word_id = next_word.id if next_word else None
    return render(request, 'compare_audio.html', {
        'word': word,
        'recordings': recordings,
        'next_word_id': next_word_id
    })
    

# AI Assessment on user recordings

# client = OpenAI(api_key="sk-proj-8tsKt51ax7c9AoOO3RYST3BlbkFJkVGybZPjPoHTxK1LZXIm")

AI_FEEDBACK_100 = [
    "Great job! Your pronunciation of '{word}' sounds just like a native American speaker! 🎉🎤",
    "Excellent! You nailed the American accent for '{word}'. Keep up the good work! 🌟👏",
    "Fantastic! Your pronunciation of '{word}' was spot on with an American accent. You're making great progress! 🚀😊",
    "Awesome work! Your American accent while saying '{word}' is really impressive. Keep practicing, and you'll be fluent in no time! 🎶👍",
    "Perfect! You pronounced '{word}' perfectly. Keep it up, and you'll master the American accent! 💯🎧",
    "Amazing! Your pronunciation of '{word}' is flawless. You're doing an incredible job! 🏆🎤",
    "Impressive! You said '{word}' just like a native speaker. Keep shining! 🌟🎤",
    "Superb! Your American accent for '{word}' is spot on. Keep practicing, and you'll achieve even greater fluency! 🥇🌟",
    "Wonderful! Your pronunciation of '{word}' is perfect. You're becoming a pro at this! 👏🎤",
    "Outstanding! You pronounced '{word}' exactly right. Keep up the fantastic work! 🌟🎉",
    "Great job! Your pronunciation of '{word}' sounds just like a native American speaker! 👏",
    "Excellent! You nailed the American accent for '{word}'. Keep up the good work 👌!",
    "Fantastic! Your pronunciation of '{word}' was spot on with an American accent. You're making great progress! 🌟", 
    "Awesome work! Your American accent while saying '{word}' is really impressive. Keep practicing, and you'll be fluent in no time! 💯🎧", 
    ]

AI_FEEDBACK_0 = [
    "Good effort! Your pronunciation of '{word}' was very close to native. 👌 ",
    "You're on the right track! Your accent for '{word}' is improving. 🚀",
    "Nice try! Your pronunciation of '{word}' was almost perfect. 🌟",
    "Great job! Your American accent for '{word}' is coming along. 👏",
    "Well done! Your attempt at '{word}' was quite close. 🎵",
    "Good attempt! Your pronunciation of '{word}' is getting better. 💪 ",
    "Good effort! Your pronunciation of '{word}' is almost there. Keep practicing, and you'll get it perfect in no time! 👍",
    "Nice try! You're getting closer with your pronunciation of '{word}'. Focus on the ending sound to make it even better. 💪",
    "You're doing great! With a bit more practice, your pronunciation of '{word}' will be spot on. Keep it up! 🌟",
    "Great attempt! Your pronunciation of '{word}' is improving. Pay attention to the vowel sounds for a more accurate accent. 👂",
    "Well done! Your effort in pronouncing '{word}' is clear. Keep practicing the tricky parts, and you'll master it soon! 👏",
    "You're making progress! With just a bit more practice, your pronunciation of '{word}' will be excellent. Don't give up! 🚀",
    "Good job! Your pronunciation of '{word}' is getting better. Keep working on the consonant sounds for a perfect accent. 👌",
    "Nice effort! You're on the right track with your pronunciation of '{word}'. Focus on the rhythm and stress for an even better result. 🎯",
    "You're almost there! Keep practicing '{word}' and pay attention to the intonation. You're doing great! 🎵",
    "Great work! Your pronunciation of '{word}' is coming along nicely. Keep practicing, and you'll sound like a native speaker soon! 🗣️",



]

class SpeechToTextView(View):
    def get(self, request, word_id):
        word = get_object_or_404(Word, id=word_id)
        assess_next_word = Word.objects.filter(id__gt=word_id).order_by('id').first()
        assess_previous_word = Word.objects.filter(id__lt=word_id).order_by('-id').first()
        assess_next_word_id = assess_next_word.id if assess_next_word else None
        assess_previous_word_id = assess_previous_word.id if assess_previous_word else None
        
        context = {
            'word': word,
            'assess_next_word_id': assess_next_word_id,
            'assess_previous_word_id': assess_previous_word_id,
        }
        
        return render(request, 'speech_to_text.html', context)

    def post(self, request, word_id):
        if 'audio_data' not in request.FILES:
            return HttpResponseBadRequest('Audio file not found')

        audio_file = request.FILES['audio_data']
        word = get_object_or_404(Word, id=word_id)

        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            for chunk in audio_file.chunks():
                tmp_file.write(chunk)
            tmp_file_path = Path(tmp_file.name)

        # Transcribe using OpenAI
        client = OpenAI(api_key="sk-proj-8tsKt51ax7c9AoOO3RYST3BlbkFJkVGybZPjPoHTxK1LZXIm")

        try:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=tmp_file_path,
                response_format="text"
            )
            transcription = response  # response is already a string
            feedback = None
            if transcription.lower() == word.text.lower():
                feedback = random.choice([fb.format(word=word.text) for fb in AI_FEEDBACK_100])
            elif transcription.lower() != word.text.lower():
                feedback = random.choice([fb.format(word=word.text) for fb in AI_FEEDBACK_0])

            # Remove the temporary file
            os.remove(tmp_file_path)

            return JsonResponse({
                'transcription': transcription,
                'feedback': feedback,
            })
        except openai.error.APIConnectionError as e:
            return JsonResponse({
                'error': 'Connection error.'
            }, status=500)
        except openai.error.APIError as e:
            return JsonResponse({
                'error': str(e)
            }, status=500)
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            }, status=500)
 