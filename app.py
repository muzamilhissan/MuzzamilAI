import streamlit as st
import speech_recognition as sr
import google.generativeai as genai
from gtts import gTTS
import os
import tempfile

# Configure API key for Google Generative AI
api_key = "AIzaSyALowN1vb7OcYmbkvUdnyboC_MeX5jGWYQ"  # Replace with your actual API key
genai.configure(api_key=api_key)

# Specify the model name (Gemini 2.0 Flash)
model_name = "gemini-2.0-flash"  # Model you want to use

# Speech-to-text function for audio file uploads
def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    try:
        # Recognize speech from the uploaded file
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)  # Capture the audio from the file
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

# Convert text to speech using gTTS
def text_to_speech(text):
    try:
        tts = gTTS(text)
        # Save the speech as an audio file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name + ".mp3"
            tts.save(temp_file_path)
            st.audio(temp_file_path, format='audio/mp3')
    except Exception as e:
        st.error(f"An error occurred while converting text to speech: {e}")

# Streamlit app UI
def main():
    st.title("Speech to Text, Text Generation & Speech Response App")

    # Option to upload an audio file
    audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])
    
    if audio_file is not None:
        # Display the uploaded file
        st.audio(audio_file, format="audio/wav")

        # Convert speech to text
        recognized_text = speech_to_text(audio_file)
        if recognized_text:
            # Send recognized text to Gemini model and get response
            generated_text = generate_text_from_gemini(recognized_text)
            if generated_text:
                # Convert the generated text to speech
                text_to_speech(generated_text)

if __name__ == "__main__":
    main()
