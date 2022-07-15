import os

import imageio.v3 as iio
from flask import Flask, jsonify, url_for, request
from flask_cors import CORS

app = Flask(
    __name__,
    static_url_path='/static',
    static_folder='static'
)
CORS(app)


@app.route('/api/videos')
def videos_list():
    files = os.listdir('static/videos')
    return jsonify(files)


@app.route('/api/videos/<filename>')
def videos_get(filename):
    return jsonify(
        name=filename,
        url=url_for('static', filename=f'videos/{filename}')
    )


@app.route('/api/videos/<filename>/frames')
def video_get_frames(filename):
    _VIDEO_FRAME_RATE = 23.98

    timecode = float(request.args.get('timecode'))
    key_frame_index = int(timecode * _VIDEO_FRAME_RATE)

    result = []
    for index in range(key_frame_index - 5, key_frame_index + 7):
        try:
            frame = iio.imread(f'static/videos/{filename}', index=index)
            binary_image = iio.imwrite('<bytes>', frame, extension='.png')
            result.append(binary_image.decode('ISO-8859-1'))
        except:
            pass

    return jsonify(result)


if __name__ == '__main__':
    app.run()
