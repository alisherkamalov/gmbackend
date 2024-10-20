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

    # Путь для сохранения аудио
    audio_path = f"downloads/{os.path.basename(video_url)}.mp3"

    # Настройки для yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': audio_path,
        'noplaylist': True,
        'quiet': True,
    }

    try:
        # Загружаем аудио
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Проверяем, что файл был создан
        if os.path.exists(audio_path):
            # Возвращаем ссылку на файл
            response = jsonify({'audio_url': audio_path})
            # Удаляем файл после отправки ответа
            @response.call_on_close
            def remove_file():
                try:
                    os.remove(audio_path)
                    print(f'Файл {audio_path} успешно удален.')
                except Exception as e:
                    print(f'Ошибка при удалении файла: {str(e)}')

            return response, 200
        else:
            return jsonify({'error': 'Ошибка загрузки аудиофайла'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Создаем директорию для загрузок, если ее нет
    os.makedirs('downloads', exist_ok=True)
    app.run(debug=True, port=5000)
