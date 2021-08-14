import datetime
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


def run(email):
    nltk.download('vader_lexicon')
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(email)
    print(scores)
    return scores


def plot_scores(scores):    
    labels = list(scores.keys())
    label_popped = labels.pop(-1)
    
    vals = list(scores.values())
    vals_popped = vals.pop(-1)
    
    plt.style.use('fivethirtyeight')

    fig1, ax1 = plt.subplots()
    ax1.pie(vals, labels=labels, autopct='%1.1f%%',
            startangle=90, pctdistance=0.8)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # ax1.set_title("Sentiment Analysis of Emails")
    
    return fig1


def plot_scores_px(scores):    
    labels = list(scores.keys())
    label_popped = labels.pop(-1)
    
    vals = list(scores.values())
    vals_popped = vals.pop(-1)
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=vals)])
    
    return fig


def plot_totals_px(scores):    
    labels = list(scores.keys())
    
    vals = list(scores.values())
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=vals)])
    
    return fig


def sentiment_func(scores):
    
    vals = list(scores.values())
    comp_val = vals.pop(-1)
    
    if comp_val >= 0.05:
        sentiment = 'positive'
    elif (comp_val > -0.05) and (comp_val < 0.05):
        sentiment = "neutral"
    else:
        sentiment = "negative"
        
    return sentiment


def return_datetime(date):
    
    yr = int(date.split('-')[0])
    month = int(date.split('-')[1].strip("0"))
    day = int(date.split('-')[2].strip("0"))
    datetime_date = datetime.date(yr, month, day)
    
    return datetime_date

    