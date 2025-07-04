# Sentimental-Analysis
A modern and intuitive X-ray Analyzer UI that allows users to upload X-ray images, enhance them to reduce noise, segment and outline each bone clearly, and detect cracks using visual indicators like circles. The interface features a clean medical theme with interactive tools and layered image views for detailed analysis.
🎭 Emotion-Based Music & Netflix Recommendation System
This project uses facial emotion recognition to give personalized Spotify music and Netflix show recommendations based on your mood — all through your webcam!

💡 Features
📸 Capture your face using your webcam (via Google Colab)
🧠 Analyze emotions using DeepFace
🎵 Recommend mood-matching Spotify songs (international + Bollywood)
🎬 Recommend Netflix titles from a dataset of 8,000+ shows
📊 View a bar chart of your detected emotional breakdown

🚀 How It Works
Upload the netflix_titles.csv dataset.
Provide your Spotify API credentials.
Capture a photo using your webcam.
Let the system detect your dominant emotion.
Enjoy tailored Netflix and Spotify recommendations!

📦 Tech Stack
Python
Google Colab
DeepFace (for emotion analysis)
OpenCV + JS (for webcam)
Spotify Web API (via spotipy)
Pandas, NumPy, Matplotlib

🛠 Requirements
Install dependencies using:
python
Copy
Edit
!pip install deepface spotipy pandas numpy opencv-python-headless
!apt-get install python3-opencv -y

📂 Dataset
Please upload netflix_titles.csv. You can get it from:
Netflix Dataset on Kaggle

🔐 Spotify API Setup
Visit Spotify Developer Dashboard

Create a new app and copy the Client ID and Client Secret

Paste them when prompted

👩‍💻 Run on Google Colab
This project is designed to run in Google Colab for easy webcam access.
