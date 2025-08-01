import os
import sounddevice as sd
import numpy as np
import wavio
from gtts import gTTS
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory, LangDetectException

# ✅ Ensure consistent language detection results
DetectorFactory.seed = 0

# ✅ Set proper directory paths
OUTPUT_DIR = "outputs"
AUDIO_FILE = os.path.join(OUTPUT_DIR, "voice_input.wav")

def record_audio(duration=5, samplerate=44100):
    """Records audio and saves it as WAV."""
    print("Recording...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    
    # ✅ Save the audio properly
    wavio.write(AUDIO_FILE, audio, samplerate, sampwidth=2)
    
    # ✅ Play back the recorded audio
    print("Playing back the recorded audio...")
    os.system(f"start {AUDIO_FILE}")
    
    return AUDIO_FILE


def translate_voice(target_language):
    """Recognize speech, translate, and generate audio."""
    audio_file = record_audio()

    from speech_recognition import Recognizer, AudioFile, UnknownValueError, RequestError
    
    recog = Recognizer()
    
    # Recognize speech from audio file
    with AudioFile(audio_file) as source:
        audio = recog.record(source)

    try:
        recognized_text = recog.recognize_google(audio)
        print("Recognized:", recognized_text)
    except UnknownValueError:
        print("Could not understand the audio.")
        return None, None, None
    except RequestError as e:
        print(f"Google Speech Recognition request failed: {e}")
        return None, None, None
    
    if recognized_text:
        print(f"Detecting language for text: {recognized_text}")

        # ✅ Language detection using `langdetect`
        try:
            detected_language = detect(recognized_text)
            print(f"Detected Language: {detected_language}")
        except LangDetectException:
            print("Language detection failed. Using fallback: 'en'")
            detected_language = 'en'

        # ✅ Translate to target language
        translated_text = GoogleTranslator(source=detected_language, target=target_language).translate(recognized_text)
        print(f"Translated: {translated_text}")

        # ✅ Save translated audio to correct path
        output_audio_file = os.path.join(OUTPUT_DIR, f"captured_voice_{target_language}.mp3")
        tts = gTTS(translated_text, lang=target_language)
        tts.save(output_audio_file)

        # ✅ Return correct file path and translated text
        return recognized_text, translated_text, f"/static/outputs/{os.path.basename(output_audio_file)}"

    else:
        print("No recognizable speech detected.")
        return None, None, None
