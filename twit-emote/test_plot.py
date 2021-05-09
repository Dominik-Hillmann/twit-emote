import plotly.graph_objects as go
import os
import pandas as pd

# df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/polar_dataset.csv")

print(['Happy', 'Sad', 'Angry', 'Surprise', 'Fear'],
('Emotions', [
    [0.88, 0.01, 0.03, 0.03, 0.00],
    [0.07, 0.95, 0.04, 0.05, 0.00],
    [0.01, 0.02, 0.85, 0.19, 0.05],
    [0.02, 0.01, 0.07, 1.00, 0.21],
    [0.01, 0.01, 0.02, 0.71, 0.74]
]))

emo_types = ['Happy', 'Sad', 'Angry', 'Surprise', 'Fear']
emotions = pd.DataFrame([
    ['The name', 0.88, 0.01, 0.03, 0.03, 0.00],
    ['The name', 0.07, 0.95, 0.04, 0.05, 0.00],
    ['The name', 0.01, 0.02, 0.85, 0.19, 0.05],
    ['The name', 0.02, 0.01, 0.07, 1.00, 0.21]
], columns = ['Handle'] + emo_types)
print(emotions)
# print(df)


fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r = [0.88, 0.1, 0.3, 0.3, 0.1, 0.88],
    theta = ['Happy', 'Sad', 'Angry', 'Surprise', 'Fear', 'Happy'],
    mode = 'lines',
    line_color = 'peru'
))

fig.add_trace(go.Scatterpolar(
    r = [0.01, 0.02, 0.85, 0.19, 0.05, 0.01],
    theta = ['Happy', 'Sad', 'Angry', 'Surprise', 'Fear', 'Happy'],
    mode = 'lines',
    fill = "toself",
    fillcolor = '#709BFF',
    line_color = 'lightblue'
))


fig.update_layout(
    showlegend = False,
    template = 'plotly_dark'
)
if not os.path.exists('img'):
    os.mkdir('img')

fig.write_image(os.path.join('img', 'test.jpg'))
# fig.show()