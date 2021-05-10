"""This file contains the function to create the radar plot."""
import plotly.graph_objects as go
import os
import pandas as pd

from typing import Dict, List

def to_ordered_emotions_list(emotions_dict: Dict[str, float]) -> List[float]:
    return [
        emotions_dict['Happy'],
        emotions_dict['Sad'],
        emotions_dict['Angry'],
        emotions_dict['Surprise'],
        emotions_dict['Fear'],
        emotions_dict['Happy'] # To connect last line, repeat first value (and key).
    ]


def create_plot(
    filename: str,
    emotions: List[Dict[str, float]],
    emotion_types: List[str] = ['Happy', 'Sad', 'Angry', 'Surprise', 'Fear'],
    dir_name: str = 'img'    
) -> None:
    # Attach first element as last to connect the last line.
    # emotion_types += emotion_types[0]

    fig = go.Figure()
    for emotion_dict in emotions:
        emotions_ordered = to_ordered_emotions_list(emotion_dict)
        
        fig.add_trace(go.Scatterpolar(
            r = emotions_ordered,
            theta = emotion_types + [emotion_types[0]],
            mode = 'lines'
        ))
    

    fig.update_layout(showlegend = False, template = 'plotly_dark')
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    fig.write_image(os.path.join(dir_name, filename))


# fig.add_trace(go.Scatterpolar(
#     r = [0.88, 0.1, 0.3, 0.3, 0.1, 0.88],
#     theta = ['Happy', 'Sad', 'Angry', 'Surprise', 'Fear', 'Happy'],
#     mode = 'lines',
#     line_color = 'peru'
# ))

# fig.add_trace(go.Scatterpolar(
#     r = [0.01, 0.02, 0.85, 0.19, 0.05, 0.01],
#     theta = ['Happy', 'Sad', 'Angry', 'Surprise', 'Fear', 'Happy'],
#     mode = 'lines',
#     fill = "toself",
#     fillcolor = '#709BFF',
#     line_color = 'lightblue'
# ))


# fig.show()