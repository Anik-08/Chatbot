from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging
import markdown

# Set up logging
logger = logging.getLogger(__name__)

load_dotenv()

# Configure the Gemini API
try:
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro')
    logger.info("Gemini API configured successfully")
except Exception as e:
    logger.error(f"Error configuring Gemini API: {str(e)}")
    raise

def home(request):
    return render(request, 'chatbot_app/home.html')

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        try:
            user_message = request.POST.get('message', '')
            logger.info(f"Received message: {user_message}")
            
            if not user_message:
                return JsonResponse({'error': 'Message cannot be empty'}, status=400)
            
            try:
                # Generate the response using Gemini API
                response = model.generate_content(user_message)
                logger.info("Successfully got response from Gemini API")
                
                if response.text:
                    # Convert markdown to HTML
                    html_response = markdown.markdown(response.text)
                    return JsonResponse({'response': html_response})
                else:
                    logger.error("Empty response from Gemini API")
                    return JsonResponse({'error': 'No response from Gemini API'}, status=500)
            except Exception as e:
                logger.error(f"Error generating content: {str(e)}")
                return JsonResponse({'error': str(e)}, status=500)
        except Exception as e:
            logger.error(f"Unexpected error in chat view: {str(e)}")
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)
