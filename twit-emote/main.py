import text2emotion
from fastapi import FastAPI
import twitter
from dotenv import load_dotenv
import os
import text2emotion as t2e


from test_plot import plot_radar
# Libraries
import matplotlib.pyplot as plt
# import pandas as pd
from math import pi

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

@app.get('/radar/{handle}')
def create_radar_graph(handle: str) -> None:
    try:
        statuses = twitter_api.GetUserTimeline(screen_name = handle)
    except NameError as e:
        return { 'error': f'User {handle} does not exist: {e}' }

    print([s.text for s in statuses])
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
    print([happy / sum_emotions, angry / sum_emotions, surprise / sum_emotions, sad / sum_emotions, fear / sum_emotions])
    emotions = [
        happy / sum_emotions, 
        angry / sum_emotions, 
        surprise / sum_emotions, 
        sad / sum_emotions, 
        fear / sum_emotions
    ]
    print(sum_emotions)
    plot_radar(emotions)


    return { 
        'name': handle,
        'length': len(statuses),
        'tweets': [
            happy / sum_emotions, 
            angry / sum_emotions, 
            surprise / sum_emotions, 
            sad / sum_emotions, 
            fear / sum_emotions
        ]#,
        # 'emotions': [ t2e.get_emotion(s.text) for s in statuses ]
    }
