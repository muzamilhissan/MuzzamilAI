import streamlit as st
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai
import os

# Configure API key for Google Generative AI
api_key = "AIzaSyALowN1vb7OcYmbkvUdnyboC_MeX5jGWYQ"  # Replace with your actual API key
genai.configure(api_key=api_key)

# Specify the model name (Gemini 2.0 Flash)
model_name = "gemini-2.0-flash"  # Model you want to use

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init()

# Speech-to-text function using the microphone
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening for your speech...")
        audio = recognizer.listen(source)
    try:
        st.info("Recognizing speech...")
        text = recognizer.recognize_google(audio)
        st.success(f"Recognized Text: {text}")
        return text
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Text generation using Gemini model
def generate_text_from_gemini(prompt):
    try:
        response = genai.generate_text(model=model_name, prompt=prompt)
        generated_text = response['text']
        st.success(f"Generated Text: {generated_text}")
        return generated_text
    except Exception as e:
        st.error(f"An error occurred while generating text: {e}")
        return None

# Convert text to speech
def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

# Streamlit app UI
def main():
    st.title("Speech to Text, Text Generation & Speech Response App")

    # Option to record speech
    if st.button("Record Speech"):
        recognized_text = speech_to_text()
        if recognized_text:
            # Send recognized text to Gemini model and get response
            generated_text = generate_text_from_gemini(recognized_text)
            if generated_text:
                # Convert the generated text to speech
                text_to_speech(generated_text)

if __name__ == "__main__":
    main()
