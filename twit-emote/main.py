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
import numpy as np
import cv2

import requests
from PIL import Image, ImageDraw

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
def create_radar_graph(handles: str) -> FileResponse:
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
        except twitter.error.TwitterError as e:
            return { 'error': f'User {handle} does not authorize API access.' }

        # print([s.text for s in statuses])
        
        profile_url = twitter_api.GetUser(screen_name = handles[0]).profile_image_url
        profile_img = Image.open(requests.get(profile_url, stream=True).raw)
        profile_img = crop_circular(profile_img)
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
        try:
            emotions = {
                'Happy': happy / sum_emotions, 
                'Angry': angry / sum_emotions, 
                'Surprise': surprise / sum_emotions, 
                'Sad': sad / sum_emotions, 
                'Fear': fear / sum_emotions
            }

            emotions_collector.append(emotions)
        except ZeroDivisionError:
            continue

    create_plot(filename, emotions_collector)

    radar = Image.open(os.path.join('img', filename))

    radar.paste(profile_img, (1, 1))
    radar.save(os.path.join('img', 'radar.png'))

    return FileResponse(os.path.join('img', filename))




def crop_circular(img: Image.Image) -> Image.Image:
    # background = Image.new('RGBA', (50, 50), color = 0)
    # background = cv2.circle(
    #     np.array(background), 
    #     (25, 25), 
    #     25, 
    #     'red', 
    #     30
    # )
    # Center coordinates

    background = np.zeros((64, 64, 3), np.uint8)
    center_coordinates = (32, 32)
    
    # Radius of circle
    radius = 32
    
    # Red color in BGR
    color = (255, 0, 0)
    
    # Line thickness of -1 px
    thickness = -1
    
    # Using cv2.circle() method
    # Draw a circle of red color of thickness -1 px
    background = cv2.circle(background, center_coordinates, radius, color, thickness)
    

    # img = cv2.imread('lena.jpg')
    img = np.array(img)
    hh, ww = img.shape[:2]
    hh2 = hh // 2
    ww2 = ww // 2

    # define circles
    radius1 = 25
    radius2 = 75
    xc = hh // 2
    yc = ww // 2

    # # draw filled circles in white on black background as masks
    mask1 = np.zeros_like(img)
    mask1 = cv2.circle(mask1, (xc, yc), radius1, (255, 255, 255), -1)
    mask2 = np.zeros_like(img)
    mask2 = cv2.circle(mask2, (xc, yc), radius2, (255, 255, 255), -1)

    # subtract masks and make into single channel
    mask = cv2.subtract(mask2, mask1)
    mask = 255 - mask

    # put mask into alpha channel of input
    result = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    result[:, :, 3] = mask[:, :, 0]

    result = Image.fromarray(result)
    ImageDraw.floodfill(result, (1, 1), (255, 255, 0, 0))

    # background = cv2.cvtColor(background, cv2.COLOR_BGR2BGRA)
    # background[7:55, 7:55, :] = result
    return result




    # return Image.fromarray(image)



    # npImage=np.array(img)
    # h, w=img.size

    # # Create same size alpha layer with circle
    # alpha = Image.new('L', img.size,0)
    # draw = ImageDraw.Draw(alpha)
    # draw.pieslice([0,0,h,w],0,360,fill=255)

    # # Convert alpha Image to numpy array
    # npAlpha=np.array(alpha)

    # # Add alpha layer to RGB
    # npImage=np.dstack((npImage,npAlpha))
    # print(npImage, npImage.shape)

    # # Save with alpha
    # Image.fromarray(npImage).save('result.png')