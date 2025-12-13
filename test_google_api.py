import google.generativeai as genai

genai.configure(api_key='AIzaSyDXrVBdPxxpA7Qjg7iS552b2u9u3B2LiFw')

# List available models
print("Available models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"  - {m.name}")

# Test with a simple query
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("Say hello")
print("\nTest response:")
print(response.text)
