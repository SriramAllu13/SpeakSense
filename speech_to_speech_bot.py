import streamlit as st
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai

# Initializing the speech recognition
recognizer = sr.Recognizer()

# Initializing text-to-speech engine
engine = pyttsx3.init()

# Configuring Gemini API  with a API key
API_KEY = "AIzaSyAMVAqYsC48uTF7lWySay3sZktSjR2uurs"
genai.configure(api_key=API_KEY)

# Using Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit UI
st.title("Speech-to-Speech LLM Bot")

# Capturing Speech Input
def capture_speech():
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source, phrase_time_limit=3)
        
    try:
        text = recognizer.recognize_google(audio)
        st.write(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        st.write("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        st.write("Request to Google API failed.")
        return None

# Generating Response using Gemini
def generate_response(prompt):
    response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(
        max_output_tokens=50,
    ))  
    return response.text

# Converting Text to Speech
def speak_text(text):
    if engine._inLoop:  
        engine.endLoop()
    engine.say(text)
    engine.runAndWait()

# Main Function
def main():
    st.write("Click the button below and speak into your microphone.")
    if st.button("Start Listening"):
        # Step 1: Capturing speech input
        user_input = capture_speech()
        
        if user_input:
            if "stop" in user_input.lower():
                st.write("Stopping the bot as requested.")
                speak_text("Goodbye!")
                return
            
            # Step 2: Generating response using Gemini
            response = generate_response(user_input)
            
            # Step 3: Output the response as speech
            st.write(f"Bot: {response}")
            speak_text(response)

if __name__ == "__main__":
    main()
