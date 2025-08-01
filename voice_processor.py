import os
import numpy as np
import sounddevice as sd
import wavio
import speech_recognition as sr
from deep_translator import GoogleTranslator, single_detection
from gtts import gTTS

# Constants
AUDIO_FOLDER = "outputs"
AUDIO_FILE = os.path.join(AUDIO_FOLDER, "voice_input.wav")

# Ensure the outputs folder exists
if not os.path.exists(AUDIO_FOLDER):
    os.makedirs(AUDIO_FOLDER)

# Function to record audio
def record_audio(duration=5, samplerate=44100):
    print("Recording...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    return np.squeeze(audio)

# Function to save audio as WAV
def save_audio(audio, filename=AUDIO_FILE, samplerate=44100):
    wavio.write(filename, audio, samplerate, sampwidth=2)

# Function to recognize speech
def recognize_speech(wav_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_file) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        return None

# Function to translate text
def translate_text(text, target_language):
    try:
        detected_lang = single_detection(text, api_key='auto')
        translated = GoogleTranslator(source=detected_lang, target=target_language).translate(text)
        return detected_lang, translated
    except Exception as e:
        print(f"Translation error: {e}")
        return None, None

# Function to convert text to speech
def text_to_speech(text, lang, output_file):
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(output_file)
        return output_file
    except Exception as e:
        print(f"TTS error: {e}")
        return None
