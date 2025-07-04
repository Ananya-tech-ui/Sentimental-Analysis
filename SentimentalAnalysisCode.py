!pip install deepface spotipy pandas numpy opencv-python-headless
!apt-get install python3-opencv -y

import pandas as pd
import numpy as np
from deepface import DeepFace
import cv2
import matplotlib.pyplot as plt
from IPython.display import display, Javascript, Image, HTML
from google.colab.output import eval_js
from base64 import b64decode, b64encode
import os
import io
import PIL
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from google.colab import files

print("Please upload the netflix_titles.csv file")
uploaded = files.upload()

def load_netflix_dataset():
    try:
        df = pd.read_csv('netflix_titles.csv')
        df['listed_in'] = df['listed_in'].fillna('')
        df['description'] = df['description'].fillna('')
        df['type'] = df['type'].fillna('Unknown')
        print(f"Successfully loaded Netflix dataset with {len(df)} titles.")
        return df
    except Exception as e:
        print(f"Error loading Netflix dataset: {e}")
        return None

def setup_spotify():
    client_id = input("Enter your Spotify Client ID: ")
    client_secret = input("Enter your Spotify Client Secret: ")

    try:
        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        sp.search(q='test', limit=1)
        return sp
    except Exception as e:
        print(f"Error connecting to Spotify: {e}")
        return None

def take_photo(filename='photo.jpg', quality=0.8):
    js = Javascript('''
        async function takePhoto(quality) {
            const div = document.createElement('div');
            const capture = document.createElement('button');
            capture.style.backgroundColor = '#4CAF50';
            capture.style.border = 'none';
            capture.style.color = 'white';
            capture.style.padding = '15px 32px';
            capture.style.textAlign = 'center';
            capture.style.textDecoration = 'none';
            capture.style.display = 'inline-block';
            capture.style.fontSize = '16px';
            capture.style.margin = '4px 2px';
            capture.style.cursor = 'pointer';
            capture.style.borderRadius = '4px';

            const warning = document.createElement('div');
            warning.style.color = 'red';
            warning.style.marginBottom = '10px';
            warning.innerHTML = 'Please allow camera access when prompted.';

            capture.textContent = 'Capture Photo';
            div.appendChild(warning);
            div.appendChild(capture);

            const video = document.createElement('video');
            video.style.display = 'block';
            video.style.marginBottom = '10px';

            try {
                const stream = await navigator.mediaDevices.getUserMedia({video: true});
                document.body.appendChild(div);
                div.appendChild(video);
                video.srcObject = stream;
                await video.play();

                google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);

                await new Promise((resolve) => capture.onclick = resolve);

                const canvas = document.createElement('canvas');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                canvas.getContext('2d').drawImage(video, 0, 0);
                stream.getVideoTracks()[0].stop();
                div.remove();
                return canvas.toDataURL('image/jpeg', quality);
            } catch (err) {
                div.remove();
                throw new Error('Camera permission denied or error occurred: ' + err.message);
            }
        }
    ''')

    try:
        display(js)
        data = eval_js('takePhoto({})'.format(quality))
        binary = b64decode(data.split(',')[1])
        with open(filename, 'wb') as f:
            f.write(binary)
        return filename
    except Exception as e:
        print("Error in capturing photo:", str(e))
        return None

def get_netflix_recommendations(emotion, df):
    emotion_mapping = {
        'happy': {
            'genres': ['Comedies', 'Stand-Up Comedy', 'Children', 'Family'],
            'keywords': ['funny', 'happy', 'cheerful', 'comedy', 'family']
        },
        'sad': {
            'genres': ['Dramas', 'Romantic', 'Documentaries'],
            'keywords': ['emotional', 'drama', 'touching', 'romantic']
        },
        'angry': {
            'genres': ['Action', 'Thrillers', 'Crime'],
            'keywords': ['action', 'thriller', 'intense', 'revenge']
        },
        'neutral': {
            'genres': ['Documentaries', 'Science & Nature', 'Food & Wine'],
            'keywords': ['documentary', 'educational', 'nature', 'science']
        },
        'fear': {
            'genres': ['Horror', 'Thrillers', 'Supernatural'],
            'keywords': ['horror', 'scary', 'thriller', 'supernatural']
        },
        'surprise': {
            'genres': ['Sci-Fi', 'Fantasy', 'Adventure'],
            'keywords': ['adventure', 'fantasy', 'magical', 'unexpected']
        },
        'disgust': {
            'genres': ['Horror', 'Crime', 'Thrillers'],
            'keywords': ['dark', 'disturbing', 'intense', 'crime']
        }
    }

    try:
        if df is None:
            raise Exception("Dataset not loaded")

        emotion = emotion.lower()
        mapping = emotion_mapping.get(emotion, emotion_mapping['neutral'])

        mask = df['listed_in'].str.contains('|'.join(mapping['genres']), case=False, na=False)
        mask |= df['description'].str.contains('|'.join(mapping['keywords']), case=False, na=False)

        filtered_df = df[mask].copy()

        if not filtered_df.empty:
            recommendations = filtered_df.sample(min(5, len(filtered_df)))
            return recommendations[['title', 'description', 'type', 'listed_in', 'director', 'cast']]
        return pd.DataFrame()
    except Exception as e:
        print(f"Error getting Netflix recommendations: {e}")
        return pd.DataFrame()

def get_music_recommendations(emotions, sp):
    mood_playlists = {
        'happy': [
            {'international': ['happy hits', 'feel good', 'dance pop', 'summer hits', 'party'],
             'bollywood': ['bollywood party', 'bollywood dance', 'bollywood happy', 'bollywood upbeat']},
        ],
        'sad': [
            {'international': ['sad hours', 'heartbreak', 'melancholy', 'sad beats', 'emotional'],
             'bollywood': ['bollywood sad', 'bollywood emotional', 'bollywood romance sad', 'bollywood melancholy']},
        ],
        'angry': [
            {'international': ['rage beats', 'metal', 'intense', 'rock', 'aggressive'],
             'bollywood': ['bollywood rock', 'bollywood intense', 'bollywood powerful', 'bollywood energetic']},
        ],
        'neutral': [
            {'international': ['chill hits', 'peaceful', 'relaxing', 'lofi', 'ambient'],
             'bollywood': ['bollywood classics', 'bollywood chill', 'bollywood acoustic', 'bollywood peaceful']},
        ],
        'fear': [
            {'international': ['calming', 'meditation', 'peaceful piano', 'ambient', 'soothing'],
             'bollywood': ['bollywood meditation', 'bollywood spiritual', 'bollywood calm', 'bollywood soulful']},
        ],
        'surprise': [
            {'international': ['party', 'pop hits', 'top hits', 'viral hits', 'trending'],
             'bollywood': ['bollywood trending', 'bollywood latest', 'bollywood hits', 'bollywood new']},
        ],
        'disgust': [
            {'international': ['rock', 'alternative', 'punk', 'metal', 'grunge'],
             'bollywood': ['bollywood rock', 'bollywood alternative', 'bollywood fusion', 'bollywood experimental']},
        ]
    }

    dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0].lower()

    try:
        mood = mood_playlists[dominant_emotion][0]
        songs = {'international': [], 'bollywood': []}

        # Get International songs
        for query in random.sample(mood['international'], 3):
            results = sp.search(q=query, type='track', limit=2)
            for track in results['tracks']['items']:
                if len(songs['international']) < 5:
                    songs['international'].append({
                        'name': track['name'],
                        'artist': track['artists'][0]['name'],
                        'preview_url': track['preview_url'],
                        'spotify_url': track['external_urls']['spotify']
                    })

        # Get Bollywood songs
        for query in random.sample(mood['bollywood'], 3):
            results = sp.search(q=query + " hindi", type='track', limit=2)
            for track in results['tracks']['items']:
                if len(songs['bollywood']) < 5:
                    songs['bollywood'].append({
                        'name': track['name'],
                        'artist': track['artists'][0]['name'],
                        'preview_url': track['preview_url'],
                        'spotify_url': track['external_urls']['spotify']
                    })

        return dominant_emotion, songs

    except Exception as e:
        print(f"Error getting recommendations: {e}")
        return dominant_emotion, {'international': [], 'bollywood': []}

def analyze_emotion_and_recommend(image_path, sp, netflix_df):
    try:
        result = DeepFace.analyze(image_path,
                                actions=['emotion'],
                                enforce_detection=False)

        emotions = result[0]['emotion']

        img = PIL.Image.open(image_path)
        display(img)

        plt.figure(figsize=(10, 5))
        plt.bar(emotions.keys(), emotions.values(), color='skyblue')
        plt.title('Emotion Analysis', fontsize=14, pad=20)
        plt.xlabel('Emotions', fontsize=12)
        plt.ylabel('Percentage', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

        dominant_emotion, songs = get_music_recommendations(emotions, sp)
        netflix_recommendations = get_netflix_recommendations(dominant_emotion, netflix_df)

        print(f"\n🎭 Based on your dominant emotion ({dominant_emotion.upper()}), here are your personalized recommendations:")

        print("\n🎵 International Songs:")
        for i, song in enumerate(songs['international'], 1):
            print(f"\n{i}. {song['name']} by {song['artist']}")
            print(f"   🎧 Listen on Spotify: {song['spotify_url']}")

        print("\n🎵 Bollywood Songs:")
        for i, song in enumerate(songs['bollywood'], 1):
            print(f"\n{i}. {song['name']} by {song['artist']}")
            print(f"   🎧 Listen on Spotify: {song['spotify_url']}")

        print("\n🎬 Netflix Recommendations:")
        if not netflix_recommendations.empty:
            for i, (_, row) in enumerate(netflix_recommendations.iterrows(), 1):
                print(f"\n{i}. {row['title']}")
                print(f"   📺 Type: {row['type']}")
                print(f"   🎭 Genre: {row['listed_in']}")
                print(f"   👥 Cast: {row['cast']}")
                print(f"   📝 Description: {row['description'][:200]}...")

        return emotions, songs, netflix_recommendations

    except Exception as e:
        print(f"Error in analysis: {e}")
        return None, None, None

def main():
    print("📚 Loading Netflix dataset...")
    netflix_df = load_netflix_dataset()

    print("\n🎵 Setting up Spotify...")
    sp = setup_spotify()

    if netflix_df is not None and sp is not None:
        print("\n📸 Taking photo... Click 'Capture Photo' when ready")
        photo_path = take_photo()

        if photo_path:
            print("\n🔄 Analyzing and getting recommendations...")
            analyze_emotion_and_recommend(photo_path, sp, netflix_df)
        else:
            print("❌ Failed to capture photo")
    else:
        print("❌ Failed to initialize required services")

if __name__ == "__main__":
    main()
