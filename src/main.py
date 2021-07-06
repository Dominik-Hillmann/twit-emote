import twitter
from dotenv import load_dotenv
import os
import text2emotion as t2e
import time
from flask import Flask, request, jsonify
from flask_talisman import Talisman


load_dotenv()
print(os.getenv('TOKEN'))


app = Flask(__name__)
Talisman(app)

twitter_api = twitter.Api(
    consumer_key = os.getenv('CONSUMER_API_KEY'),
    consumer_secret = os.getenv('CONSUMER_API_SECRET'),
    access_token_key = os.getenv('ACCESS_TOKEN'),
    access_token_secret = os.getenv('ACCESS_SECRET')
)

# print(twitter_api.VerifyCredentials())

@app.route('/emotions/<handles>', methods = ['GET'])
def emotions_data(handles: str):
    handles = handles.split(',')
    print(handles)

    emotions_collector = {}

    for handle in handles:
        time.sleep(1)
        print(handle)
        try:
            statuses = twitter_api.GetUserTimeline(
                screen_name = handle,
                include_rts = False
            )

        except NameError as e:
            return (
                jsonify({ 'error': f'User {handle} does not exist: {e}' }),
                500
            )

        except twitter.error.TwitterError as e:
            return (
                jsonify({ 'error': f'User {handle} does not authorize API access.' }),
                500
            )

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
        try:
            emotions = {
                'happy': happy / sum_emotions, 
                'angry': angry / sum_emotions, 
                'surprise': surprise / sum_emotions, 
                'sad': sad / sum_emotions, 
                'fear': fear / sum_emotions
            }

            emotions_collector[handle] = emotions

        except ZeroDivisionError:
            continue
        
    return jsonify(emotions_collector)


if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        port = 6000,
        debug = True
    )