import text2emotion
from fastapi import FastAPI
import twitter
from dotenv import load_dotenv
import os
import text2emotion as t2e

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
    emotions = [e / sum_emotions for e in list(emotions.values())]

    # Set data
    # df = pd.DataFrame({
    # 'group': ['A','B','C','D'],
    # 'var1': [38, 1.5, 30, 4],
    # 'var2': [29, 10, 9, 34],
    # 'var3': [8, 39, 23, 24],
    # 'var4': [7, 31, 33, 14],
    # 'var5': [28, 15, 32, 14]
    # })

    # number of variable
    categories = ['Happy', 'Angry', 'Surprise', 'Sad', 'Fear']
    N = len(categories)

    # We are going to plot the first line of the data frame.
    # But we need to repeat the first value to close the circular graph:
    # values=df.loc[0].drop('group').values.flatten().tolist()
    # values += values[:1]
    # values

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)

    # Draw one axe per variable + add labels
    plt.xticks(angles[:-1], categories, color='grey', size=8)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([10,20,30], ["10","20","30"], color="grey", size=7)
    plt.ylim(0,40)

    # Plot data
    ax.plot(angles, emotions, linewidth=1, linestyle='solid')

    # Fill area
    ax.fill(angles, emotions, 'b', alpha=0.1)

    # Show the graph
    plt.show()



    return { 
        'name': handle,
        'length': len(statuses),
        'tweets': [{ s.text: t2e.get_emotion(s.text) } for s in statuses]#,
        # 'emotions': [ t2e.get_emotion(s.text) for s in statuses ]
    }
