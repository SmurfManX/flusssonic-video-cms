from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_bootstrap import Bootstrap
from flask import send_from_directory
import os
from werkzeug.utils import secure_filename
import time
import json
from dotenv import load_dotenv 
app = Flask(__name__)

load_dotenv()

Bootstrap(app)

# Configuration constants
app.config['LOGO_FOLDER'] = os.path.join(app.root_path, 'static/thumbnails')
app.config['VIDEO_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'mp4'}

# Load and save functions for JSON files
def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json_file(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Load videos from JSON file
def load_videos():
    return load_json_file('config/db.json')

# Save videos to JSON file
def save_videos(videos):
    save_json_file(videos, 'config/db.json')

# Check if a file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    # Load videos
    videos = load_videos()
    
    if request.method == 'POST':
        # Process uploaded files
        file = request.files['video_file']
        logo = request.files['logo']
        file_name = request.form['file_name']

        if file and allowed_file(file.filename) and logo:
            # Save files and update video data
            date_folder = time.strftime('%Y-%m-%d')
            video_folder = os.path.join(app.config['VIDEO_FOLDER'], date_folder)
            os.makedirs(video_folder, exist_ok=True)

            filename = secure_filename(file.filename)
            file_path = os.path.join(video_folder, filename)
            file.save(file_path)

            logo_filename = secure_filename(logo.filename)
            logo_path = os.path.join(app.config['LOGO_FOLDER'], logo_filename)
            logo.save(logo_path)

            file_size = os.path.getsize(file_path)
            file_size_mb = round(file_size / (1024 * 1024), 10)
            upload_time = time.strftime('%Y-%m-%d')

            hls_url = f"{os.getenv('VIDEO_SERVER')}/{date_folder}/{filename}/index.m3u8"

            videos.append({
                'logo': url_for('static', filename=f'thumbnails/{logo_filename}'),
                'file_name': file_name,
                'file_path': os.path.join(date_folder, filename),
                'upload_time': upload_time,
                'file_size': file_size_mb,
                'hls_url': hls_url
            })
            save_videos(videos)
            return redirect(url_for('index'))

    # Sorting
    sort_column = request.args.get('sort', default='upload_time')
    sort_order = request.args.get('order', default='asc')

    if sort_column in ('file_name', 'upload_time', 'file_size'):
        videos.sort(key=lambda video: video[sort_column])
    if sort_order == 'desc':
        videos.reverse()
    
    return render_template('index.html', videos=videos, sort_column=sort_column, sort_order=sort_order)

@app.route('/delete/<int:video_id>', methods=['POST'])
def delete_video(video_id):
    videos = load_videos()
    
    # Check if the video_id is within valid range
    if video_id < 0 or video_id >= len(videos):
        return jsonify({'message': 'Invalid video ID'}), 400

    video = videos[video_id]
    video_path = os.path.join(app.config['VIDEO_FOLDER'], video['file_path'])
    try:
        os.remove(video_path)
    except FileNotFoundError:
        pass  # Ignore if file is not found

    # Remove logo and thumbnail
    logo_path = os.path.join(app.config['LOGO_FOLDER'], os.path.basename(video['logo']))
    thumbnail_path = os.path.join(app.config['LOGO_FOLDER'], os.path.basename(video['logo']))
    try:
        os.remove(logo_path)
        os.remove(thumbnail_path)
    except FileNotFoundError:
        pass  # Ignore if files are not found

    del videos[video_id]
    save_videos(videos)
    return redirect(url_for('index'))

@app.route('/rename_video/<int:video_id>', methods=['POST'])
def rename_video(video_id):
    new_name = request.form['new_name']

    videos = load_videos()
    videos[video_id]['file_name'] = new_name

    save_videos(videos)
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs(app.config['LOGO_FOLDER'], exist_ok=True)
    os.makedirs(app.config['VIDEO_FOLDER'], exist_ok=True)
    app.run(debug=True)
