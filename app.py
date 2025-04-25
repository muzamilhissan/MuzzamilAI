import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import google.generativeai as genai

# Google Generative AI Setup (replace with your API key)
api_key = "YOUR_GOOGLE_API_KEY"  # Replace with your actual API key
genai.configure(api_key=api_key)

# Function to convert text to speech using gTTS
def speak(text):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("output.mp3")
    os.system("start output.mp3")  # For Windows, Streamlit will stream this audio file

# Streamlit UI
st.title("Speech-to-Text with AI Response and TTS")
st.write("Upload an audio file, and the app will transcribe it and respond with speech!")

# Upload audio file
uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3"])

if uploaded_file is not None:
    st.write("File uploaded successfully!")

    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Process the audio file
    with sr.AudioFile(uploaded_file) as source:
        audio = recognizer.record(source)

    try:
        # Recognize speech and convert to text
        user_text = recognizer.recognize_google(audio)
        st.write(f"Recognized Text: {user_text}")

        # Send the recognized text to the AI model for a response
        response = genai.generate_text(prompt=user_text)

        # Show the response from the AI
        response_text = response.result
        st.write(f"AI Response: {response_text}")

        # Convert the AI response to speech
        speak(response_text)

    except sr.UnknownValueError:
        st.error("Sorry, I could not understand the speech.")
    except sr.RequestError:
        st.error("Sorry, the speech recognition service is down.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
