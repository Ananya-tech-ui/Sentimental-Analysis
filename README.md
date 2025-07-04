# 🎭 Emotion-Based Media Recommender System

**A smart system that recommends Netflix shows and Spotify music based on your current emotion detected through facial analysis**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![DeepFace](https://img.shields.io/badge/DeepFace-0.0.79-orange)
![Spotipy](https://img.shields.io/badge/Spotipy-2.22.1-green)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yourusername/repo/blob/main/Emotion_Recommender.ipynb)

## ✨ Features

- **Real-time facial emotion detection** (7 emotions: happy, sad, angry, etc.)
- **Personalized Netflix recommendations** based on detected mood
- **Custom Spotify playlists** (both International and Bollywood)
- **Interactive camera capture** directly in Colab
- **Visual emotion analysis** with bar charts
- **Comprehensive media database** integration

## 🛠️ Tech Stack

| Component          | Technology Used |
|--------------------|-----------------|
| Emotion Detection  | DeepFace        |
| Music API          | Spotify Web API |
| Data Processing    | Pandas/Numpy    |
| Image Processing   | OpenCV          |
| Visualization      | Matplotlib      |
| Web Interface      | IPython/Colab   |

## 📦 Installation (Google Colab)

```python
!pip install deepface spotipy pandas numpy opencv-python-headless
!apt-get install python3-opencv -y
🚀 Quick Start
Upload netflix_titles.csv when prompted

Enter your Spotify API credentials (Client ID and Secret)

Click "Capture Photo" to take your picture

Get personalized recommendations based on your mood!

📊 Emotion Mapping to Content
Emotion	Netflix Genres	Spotify Playlists
Happy	Comedies, Family	Dance Pop, Party Hits
Sad	Dramas, Romantic	Melancholy, Heartbreak
Angry	Action, Thrillers	Rock, Metal
Neutral	Documentaries, Science	Chill, Lo-fi
Fear	Horror, Supernatural	Calming, Meditation
Surprise	Sci-Fi, Fantasy	Trending, Viral Hits
Disgust	Crime, Thrillers	Alternative, Punk
📂 File Structure
text
emotion-recommender/
├── Emotion_Recommender.ipynb      # Main Colab notebook
├── netflix_titles.csv             # Netflix dataset
├── requirements.txt               # Python dependencies
└── README.md                      # This file
🌟 Sample Output
text
🎭 Based on your dominant emotion (HAPPY), here are your personalized recommendations:

🎵 International Songs:
1. Dance Monkey by Tones and I
   🎧 Listen on Spotify: https://open.spotify.com/track/...

🎵 Bollywood Songs:
1. Badtameez Dil by Benny Dayal
   🎧 Listen on Spotify: https://open.spotify.com/track/...

🎬 Netflix Recommendations:
1. The Mitchells vs The Machines
   📺 Type: Movie
   🎭 Genre: Children & Family Movies, Comedies
   👥 Cast: Abbi Jacobson, Danny McBride, Maya Rudolph...
   📝 Description: A quirky, dysfunctional family's road trip is upended when...
🤝 Contributing
Fork the repository

Add new emotion-content mappings

Submit a pull request
