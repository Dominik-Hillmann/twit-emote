import text2emotion
from fastapi import FastAPI
from fastapi.responses import FileResponse
import twitter
from dotenv import load_dotenv
import os
import text2emotion as t2e
import bleach
from datetime import datetime
from create_plot import create_plot
import time

import requests
from PIL import Image

load_dotenv()
print(os.getenv('TOKEN'))


app = FastAPI()
twitter_api = twitter.Api(
    consumer_key = os.getenv('CONSUMER_API_KEY'),
    consumer_secret = os.getenv('CONSUMER_API_SECRET'),
    access_token_key = os.getenv('ACCESS_TOKEN'),
    access_token_secret = os.getenv('ACCESS_SECRET')
)

# print(twitter_api.VerifyCredentials())

@app.get('/{handles}')
def create_radar_graph(handles: str) -> None:
    print(handles)
    handles = bleach.clean(handles)
    handles = handles.split(',')
    print(handles)
    filename = f'{str(datetime.now()).replace(" ", "_")}.jpg'

    emotions_collector = []
    for handle in handles:
        time.sleep(1)
        print(handle)
        try:
            statuses = twitter_api.GetUserTimeline(
                screen_name = handle,
                include_rts = False
            )
        except NameError as e:
            return { 'error': f'User {handle} does not exist: {e}' }

        # print([s.text for s in statuses])
        
        profile_url = twitter_api.GetUser(screen_name = handles[0]).profile_image_url
        profile_img = Image.open(requests.get(profile_url, stream=True).raw)
        profile_img.save(os.path.join('img', f'{handle}.png'))

        happy, angry, surprise, sad, fear = 0.0, 0.0, 0.0, 0.0, 0.0
        for status in statuses:
            tweet_text = status.text
            emotions = t2e.get_emotion(tweet_text)

            happy += emotions['Happy']
            sad += emotions['Sad']
            surprise += emotions['Surprise']
            angry += emotions['Angry']
            fear += emotions['Fear']

        sum_emotions = sum([happy, angry, surprise, sad, fear])
        emotions = {
            'Happy': happy / sum_emotions, 
            'Angry': angry / sum_emotions, 
            'Surprise': surprise / sum_emotions, 
            'Sad': sad / sum_emotions, 
            'Fear': fear / sum_emotions
        }

        emotions_collector.append(emotions)

    create_plot(filename, emotions_collector)

    return FileResponse(os.path.join('img', filename))
