from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import resolve
from contact.forms import ContactForm  
from pathlib import Path
from .models import *
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import Word, CustomerRecording
from openai import Client
from django.core.files import File
import re, os, tempfile
from django.views import View
from django.utils.decorators import method_decorator
from openai import OpenAI
import openai
from pydub import AudioSegment
from io import BytesIO
import numpy as np
from scipy.io import wavfile
import json
import pyaudio
import speech_recognition as sr
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import random
from pydub import AudioSegment
from pydub.utils import mediainfo

AudioSegment.converter = r"C:\Program Files\ffmpeg-7.0.1"


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

client = OpenAI(api_key="sk-proj-8tsKt51ax7c9AoOO3RYST3BlbkFJkVGybZPjPoHTxK1LZXIm")

class SpeechToTextView(View):
    template_name = 'speech_to_text.html'

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

        if 'media' not in request.FILES:
            return JsonResponse({"message": "No media file found"}, status=400)

        # Delete the previous recording
        CustomerRecording.objects.filter(word=word).delete()

        # Save the new recording
        media_file = request.FILES['media']
        customer_recording = CustomerRecording.objects.create(
            audio_file=media_file,
            word=word
        )

        # Save the file to a temporary location
        temp_dir = tempfile.gettempdir()
        temp_mp3_path = os.path.join(temp_dir, 'temp_audio.mp3')
        temp_wav_path = os.path.join(temp_dir, 'temp_audio.wav')
        with open(temp_mp3_path, 'wb') as f:
            f.write(media_file.read())

        # Convert MP3 to WAV
        try:
            audio = AudioSegment.from_mp3(temp_mp3_path)
            audio.export(temp_wav_path, format='wav')
        except Exception as e:
            return JsonResponse({"message": f"Error converting audio file: {str(e)}", "success": False})

        recognizer = sr.Recognizer()
        response = {"success": False, "error": None, "transcription": None}

        try:
            with sr.AudioFile(temp_wav_path) as source:
                recognizer.adjust_for_ambient_noise(source)
                audio_data = recognizer.record(source)
                response["transcription"] = recognizer.recognize_google(audio_data)
                response["success"] = True
        except sr.RequestError:
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            response["error"] = "Unable to recognize speech"
        except Exception as e:
            response["error"] = f"An unexpected error occurred: {str(e)}"

        # Clean up temporary files
        if os.path.exists(temp_mp3_path):
            os.remove(temp_mp3_path)
        if os.path.exists(temp_wav_path):
            os.remove(temp_wav_path)

        return JsonResponse(response)
    
def assess_audio(request, word_id):
        word = get_object_or_404(Word, id=word_id)
        recordings = CustomerRecording.objects.filter(word=word)
        next_word = Word.objects.filter(id__gt=word_id).order_by('id').first()
        next_word_id = next_word.id if next_word else None
        return render(request, 'assess_audio.html', {
            'word': word,
            'recordings': recordings,
            'next_word_id': next_word_id
        })