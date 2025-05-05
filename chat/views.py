from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from courses.models import Course
from .models import AIChatMessage
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import json
import os

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyBEcYe4gFqSrZ1zRJ2YMoo5NUjwOiOsU9A')
try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Test the configuration by listing available models
    model_list = genai.list_models()
    print("Available Gemini models:", [m.name for m in model_list])
except Exception as e:
    print(f"Error configuring Gemini API: {str(e)}")

@login_required
def course_chat_room(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    # Check if user is enrolled in the course
    if course.students.filter(id=request.user.id).exists() or request.user.is_staff:
        # Get chat history
        chat_history = AIChatMessage.objects.filter(
            user=request.user,
            course=course
        ).order_by('-created')[:50]  # Get last 50 messages
        return render(request, 'chat/room.html', {
            'course': course,
            'chat_history': chat_history
        })
    return JsonResponse({'error': 'You are not enrolled in this course'}, status=403)

@login_required
@csrf_exempt
def ask_ai(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '').strip()
            course = get_object_or_404(Course, id=course_id)

            if not message:
                return JsonResponse({'error': 'Message cannot be empty'}, status=400)

            try:
                # Create a new chat with Gemini
                model = genai.GenerativeModel('gemini-1.5-pro')
                
                # Generate context about the course
                context = f"You are an AI tutor for the course '{course.title}'. "
                context += f"The course overview is: {course.overview}. "
                context += "Please provide helpful and accurate responses to student questions."
                
                # Combine context and user message
                prompt = f"{context}\n\nStudent question: {message}"
                
                # Generate response from Gemini with safety settings
                safety_settings = [
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    }
                ]
                
                generation_config = {
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 1024,
                }
                
                response = model.generate_content(
                    prompt,
                    safety_settings=safety_settings,
                    generation_config=generation_config
                )
                
                if response.prompt_feedback.block_reason:
                    return JsonResponse({
                        'error': 'The request was blocked for safety reasons'
                    }, status=400)
                
                ai_response = response.text
                
                # Save the chat message
                chat_message = AIChatMessage.objects.create(
                    user=request.user,
                    course=course,
                    message=message,
                    response=ai_response
                )
                
                return JsonResponse({
                    'message': message,
                    'response': ai_response,
                    'timestamp': chat_message.created.strftime('%Y-%m-%d %H:%M:%S')
                })
                
            except Exception as e:
                print(f"Gemini API Error: {str(e)}")
                return JsonResponse({
                    'error': f'Error generating response: {str(e)}'
                }, status=500)
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)