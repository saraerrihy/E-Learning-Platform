import google.generativeai as genai
import os

def test_gemini_api():
    # Configure API
    api_key = 'AIzaSyBEcYe4gFqSrZ1zRJ2YMoo5NUjwOiOsU9A'
    print(f"Testing Gemini API with key: {api_key[:10]}...")
    
    try:
        # Configure the API
        genai.configure(api_key=api_key)
        
        # List available models
        print("\nListing available models:")
        model_list = genai.list_models()
        for model in model_list:
            print(f"- {model.name}")
        
        # Test content generation
        print("\nTesting content generation:")
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content("Say hello!")
        print(f"Response: {response.text}")
        
        print("\nAPI test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\nError testing Gemini API: {str(e)}")
        return False

if __name__ == "__main__":
    test_gemini_api() 