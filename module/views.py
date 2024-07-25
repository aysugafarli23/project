from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import resolve
from contact.forms import ContactForm  
from pathlib import Path
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Word, CustomerRecording
from openai import Client
from django.core.files import File
import re, os
from django.views import View
from django.utils.decorators import method_decorator
from openai import OpenAI
import openai
from language_tool_python import LanguageTool
import logging
from django.conf import settings
# from LangHelper.Assess import assess_transcription as langhelper_assess_transcription




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

# def transcribe_audio(audio_file_path):
#     with open(audio_file_path, 'rb') as audio_file:
#         response = client.audio.transcriptions.create(
#             file=audio_file,
#             model="whisper-1",
#             language="en",
#             temperature=0,
#             response_format="text",
#         )
      
#         transcription = response["text"]
#         return transcription

# def assess_transcription(transcription, reference_text):
#     return langhelper_assess_transcription(transcription, reference_text)


# logger = logging.getLogger(__name__)

# class PronunciationAssessmentView(View):
#     def post(self, request, word_id):
#         word = get_object_or_404(Word, id=int(word_id))
#         logger.debug("Word retrieved: %s", word.text)

#         if 'media' in request.FILES:
#             media_file = request.FILES['media']
#             logger.debug("Media file received: %s", media_file.name)

#             customer_recording = CustomerRecording.objects.create(
#                 audio_file=media_file,
#                 word=word
#             )
#             logger.debug("CustomerRecording created: %s", customer_recording.id)

#             file_path = customer_recording.audio_file.path
#             logger.debug("File path: %s", file_path)

#             try:
#                 transcription = transcribe_audio(file_path)
#                 logger.debug("Transcription: %s", transcription)

#                 assessment = assess_transcription(transcription, word.text)
#                 logger.debug("Assessment: %s", assessment)

#                 if not isinstance(assessment, dict):
#                     logger.error("Assessment is not a dictionary")
#                     return JsonResponse({'success': False, 'error': 'Invalid assessment response format'}, status=500)

#                 expected_keys = ['pronunciation_score', 'accuracy_score', 'fluency_score']
#                 for key in expected_keys:
#                     if key not in assessment:
#                         logger.error("Missing key in assessment response: %s", key)
#                         return JsonResponse({'success': False, 'error': f'Missing key in assessment response: {key}'}, status=500)

#                 response_data = {
#                     'success': True,
#                     'assessment': {
#                         'pronunciation_score': assessment['pronunciation_score'],
#                         'accuracy_score': assessment['accuracy_score'],
#                         'fluency_score': assessment['fluency_score'],
#                     }
#                 }
#                 logger.debug("Response Data: %s", response_data)
#                 return JsonResponse(response_data)
#             except Exception as e:
#                 logger.error("Error during assessment: %s", str(e))
#                 return JsonResponse({'success': False, 'error': str(e)}, status=500)

#         logger.error("No media file found in request")
#         return JsonResponse({'success': False, 'error': 'No media file found'}, status=400)

#     def get(self, request, word_id):
#         word = get_object_or_404(Word, id=word_id)
#         return render(request, 'pronunciation_assessment.html', {'word': word})
