from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from voice_translator import translate_voice
import os

app = Flask(__name__)
CORS(app)

# ✅ Create 'outputs' folder if it doesn't exist
os.makedirs('outputs', exist_ok=True)

@app.route('/translate', methods=['POST'])
def translate():
    if request.method == 'POST':
        data = request.json
        target_language = data.get('language')
        print(f"Received language: {target_language}")

        recognized_text, translated_text, audio_file_path = translate_voice(target_language)

        if recognized_text and translated_text and audio_file_path:
            return jsonify({
                'recognized_text': recognized_text,
                'translated_text': translated_text,
                'audio_file': audio_file_path
            })
        else:
            return jsonify({'error': 'Translation failed'}), 500

# ✅ Serve audio files correctly
@app.route('/static/outputs/<filename>')
def serve_audio(filename):
    return send_from_directory('outputs', filename)

if __name__ == '__main__':
    app.run(debug=True)
