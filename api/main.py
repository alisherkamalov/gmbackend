from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_audio():
    data = request.json
    video_url = data.get('url')

    if not video_url:
        return jsonify({'error': 'URL is required'}), 400

    # Настройки для yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'noplaylist': True,
        'quiet': True,
    }

    try:
        # Загружаем аудио и получаем файл
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            audio_url = info_dict['formats'][0]['url']  # Получаем ссылку на загруженное аудио

        if audio_url:
            return jsonify({'audio_url': audio_url}), 200
        else:
            return jsonify({'error': 'Ошибка загрузки аудиофайла'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
