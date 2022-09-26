#importing libraries
import streamlit as st
import numpy as np
import pandas as pd 
import os
import matplotlib.pyplot as plt
plt.style.use("seaborn-whitegrid")
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="World Ranking Universities",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.balloons()
st.title('World Ranking Universities')

st.success("Welcome to the analysis of your future! Listen to some relaxing music while exploring our page.")

#importing dataset
timesData = pd.read_csv("timesData.csv")


audio_file = open('Welcome Ringtone.oga', 'rb')
audio_bytes = audio_file.read()

st.audio(audio_bytes, format='audio/ogg')

if st.checkbox('Show head of data'):
    st.subheader('data head')
    st.write(timesData.head())


import plotly
import plotly.graph_objs as go


#Line chart:
df = timesData.iloc[:100, :]

line1 = go.Scatter(
                    x = df.world_rank,   
                    y = df.citations,    
                    mode = "lines",      
                    name = "citations",  
                    marker = dict(color = 'rgba(16, 112, 2, 0.8)'),
                    text= df.university_name)   

line2 = go.Scatter(
                    x = df.world_rank,
                    y = df.teaching,
                    mode = "lines+markers",
                    name = "teaching",
                    marker = dict(color = 'rgba(255, 0, 0, 0.8)'),
                    text= df.university_name)

data = [line1, line2]
layout = dict(title = 'Line Chart representing the Citation and Teaching vs World Rank of Top 100 Universities',
              xaxis= dict(title= 'World Rank',ticklen= 5,zeroline= False, gridcolor='rgb(248, 248, 255)')
             )

fig1 = dict(data = data, layout = layout)   

st.write(fig1)

if st.button('Explanation', 1):
    st.write('The line chart above shows that the for almost all the world ranked universities, the citations ranking was higher than the teaching ranking.This proves that the citation ranking is an important criteria for the world universities ranking.')



#Bar Chart and Line Chart
from plotly import tools
import matplotlib.pyplot as plt

df2016 = timesData[timesData.year == 2016].iloc[:7,:]

y_saving     =  [each for each in df2016.research]
y_net_worth  =  [float(each) for each in df2016.income]
x_saving     =  [each for each in df2016.university_name]
x_net_worth  =  [each for each in df2016.university_name]

trace0 = go.Bar(
                x=y_saving,
                y=x_saving,
                marker=dict(color='rgba(171, 50, 96, 0.6)',line=dict(color='rgba(171, 50, 96, 1.0)',width=1)),
                name='research',
                orientation='h',
)

trace1 = go.Scatter(
                x=y_net_worth,
                y=x_net_worth,
                mode='lines+markers',
                line=dict(color='rgb(63, 72, 204)'),
                name='income',
)

layout = dict(
                title='Bar Chart and Line Chart comparing the Research to Professors Income of top 7 Universities in 2016',
                yaxis=dict(showticklabels=True,domain=[0, 0.85]),
                yaxis2=dict(showline=True,showticklabels=False,linecolor='rgba(102, 102, 102, 0.8)',linewidth=2,domain=[0, 0.85]),
                xaxis=dict(zeroline=False,showline=False,showticklabels=True,showgrid=True,domain=[0, 0.42]),
                xaxis2=dict(zeroline=False,showline=False,showticklabels=True,showgrid=True,domain=[0.47, 1],side='top',dtick=25),
                legend=dict(x=0.029,y=1.038,font=dict(size=10) ),
                margin=dict(l=200, r=20,t=70,b=70),
                paper_bgcolor='rgb(248, 248, 255)',
                plot_bgcolor='rgb(248, 248, 255)',
)

annotations = []
y_s = np.round(y_saving, decimals=2)
y_nw = np.rint(y_net_worth)

# Adding labels
for ydn, yd, xd in zip(y_nw, y_s, x_saving):
    # labeling the scatter savings
    annotations.append(dict(xref='x2', yref='y2', y=xd, x=ydn - 4,text='{:,}'.format(ydn),font=dict(family='Arial', size=12,color='rgb(63, 72, 204)'),showarrow=False))
    # labeling the bar net worth
    annotations.append(dict(xref='x1', yref='y1', y=xd, x=yd + 3,text=str(yd),font=dict(family='Arial', size=12,color='rgb(171, 50, 96)'),showarrow=False))

layout['annotations'] = annotations

# Creating two subplots
fig2 = tools.make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                          shared_yaxes=False, vertical_spacing=0.001)

fig2.append_trace(trace0, 1, 1)
fig2.append_trace(trace1, 1, 2)

fig2['layout'].update(layout)

st.write(fig2)

if st.button('Explanation', 2):
    st.write('The figure below shows that while Harvard University has the highest research ranking, its professors income are the lowest, while the research ranking of Massachussets university is the lowerst, they have the 2nd higher income in 2016.')


df2016 = timesData[timesData.year == 2016].iloc[:7,:]
pie1 = df2016.num_students

pie1_list = [float(each.replace(',', '.')) for each in df2016.num_students] 
labels = df2016.university_name

data= [
    {
      "values": pie1_list,
      "labels": labels,
      "domain": {"x": [0, .5]},
      "name": "Number Of Students Rates",
      "hoverinfo":"label+percent+name",
      "hole": .05,
      "type": "pie"
    }]

layout={
        "title":"Pie Chart representing the Students rate of top 7 Universities in 2016",
        "annotations": [
            { "font": { "size": 20},
              "showarrow": False,
              "text": "Number of Students",
                "x": 0.20,
                "y": 1
            },
        ]
    }

fig3 = go.Figure(data=data, layout=layout)

st.write(fig3)

if st.button('Explanation', 3):
    st.write('The pie chart above shows that the highest rate of students is found in Harvard University, while the lowest rate of students is found in California Insitute of Technology.')


#Pie Chart
import plotly.figure_factory as ff

dataframe = timesData[timesData.year == 2015]
data2015 = dataframe.loc[:,["research","international", "total_score"]]
data2015["index"] = np.arange(1,len(data2015)+1)

fig4 = ff.create_scatterplotmatrix(data2015, diag='box', index='index',colormap='Portland',
                                  colormap_type='cat',
                                  height=700, width=700, title = "Scatterplot Matrix representing the correlation between research, international and total score.")


#Multiple Sub-plots
trace1 = go.Scatter(
    x=dataframe.world_rank,
    y=dataframe.research,
    name = "research"
)
trace2 = go.Scatter(
    x=dataframe.world_rank,
    y=dataframe.citations,
    xaxis='x2',
    yaxis='y2',
    name = "citations"
)
trace3 = go.Scatter(
    x=dataframe.world_rank,
    y=dataframe.income,
    xaxis='x3',
    yaxis='y3',
    name = "income"
)
trace4 = go.Scatter(
    x=dataframe.world_rank,
    y=dataframe.total_score,
    xaxis='x4',
    yaxis='y4',
    name = "total_score"
)

data = [trace1, trace2, trace3, trace4]
layout = go.Layout(
    xaxis=dict(
        domain=[0, 0.45]
    ),
    yaxis=dict(
        domain=[0, 0.45]
    ),
    xaxis2=dict(
        domain=[0.55, 1]
    ),
    xaxis3=dict(
        domain=[0, 0.45],
        anchor='y3'
    ),
    xaxis4=dict(
        domain=[0.55, 1],
        anchor='y4'
    ),
    yaxis2=dict(
        domain=[0, 0.45],
        anchor='x2'
    ),
    yaxis3=dict(
        domain=[0.55, 1]
    ),
    yaxis4=dict(
        domain=[0.55, 1],
        anchor='x4'
    ),
    title = 'Multiple Subplots representing the Research, citation, income and total score VS World Rank of Universities'
)
fig5 = go.Figure(data=data, layout=layout)
st.write(fig5)

if st.button('Explanation', 5):
    st.write('The subplots above show that there is a positive correlation between the total score of the university rank and the income and citations they have. While there is a negative correlation between research and total income, which proves that the research has no impact on the ranking of the university if there was no citations for these researches.')


