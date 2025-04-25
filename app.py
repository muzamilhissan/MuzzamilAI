import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import google.generativeai as genai

# Google Generative AI Setup (replace with your API key)
api_key = "AIzaSyALowN1vb7OcYmbkvUdnyboC_MeX5jGWYQ"  # Replace with your API key
genai.configure(api_key=api_key)

# Function to convert text to speech using gTTS
def speak(text):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("output.mp3")
    os.system("start output.mp3")  # For Windows, Streamlit will stream this audio file

# Streamlit UI
st.title("Speech-to-Text with AI Response and TTS")
st.write("Speak to the app, and it will respond with speech!")

# Button to start speech recognition
if st.button('Start Recording'):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        st.write("Listening... Speak now.")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

    try:
        # Recognize speech and convert to text
        user_text = recognizer.recognize_google(audio)
        st.write(f"Recognized Text: {user_text}")

        # Send the recognized text to the AI model for a response (replace with your chosen model)
        chat_model = genai.ChatModel.from_pretrained("models/chat-bison")  # Example model (replace with valid model)
        response = chat_model.send_message(user_text)

        # Show the response from the AI
        response_text = response.text
        st.write(f"AI Response: {response_text}")

        # Convert the AI response to speech
        speak(response_text)

    except sr.UnknownValueError:
        st.error("Sorry, I could not understand the speech.")
    except sr.RequestError:
        st.error("Sorry, the speech recognition service is down.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

