import streamlit as st
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import os

# Your API key from https://makersuite.google.com/app/apikey
GEMINI_API_KEY = "AIzaSyALowN1vb7OcYmbkvUdnyboC_MeX5jGWYQ"
genai.configure(api_key=GEMINI_API_KEY)

st.title("Talk to AI by Muzzamil")

# Initialize TTS engine
engine = pyttsx3.init()

# Create a chat model (this avoids the error you had)
chat_model = genai.GenerativeModel("gemini-2.0-flash").start_chat(history=[])

if st.button("Start Talking"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening...")
        audio = recognizer.listen(source)
        st.success("✅ Got it! Transcribing...")

        try:
            # Speech to text
            user_text = recognizer.recognize_google(audio)
            st.text_area("You said:", user_text)

            # Send to Gemini
            st.info("Muzzamil is Thinking")
            response = chat_model.send_message(user_text)
            ai_reply = response.text
            st.text_area("Muzzamil Replied:", ai_reply)

            # Text to speech
            engine.say(ai_reply)
            engine.runAndWait()

        except sr.UnknownValueError:
            st.error("Could not understand audio.")
        except sr.RequestError as e:
            st.error(f"Error with recognition service: {e}")
