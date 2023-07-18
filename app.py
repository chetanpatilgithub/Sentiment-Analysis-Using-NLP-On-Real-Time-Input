
import re
import urllib
import bs4
import lxml
import random
import pandas as pd
import requests
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
from requests_html import HTML, HTMLSession
from textblob import TextBlob
import matplotlib
import io
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from transformers import pipeline

matplotlib.use('TkAgg')
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
classifier = pipeline("text-classification",model='bhadresh-savani/distilbert-base-uncased-emotion', return_all_scores=True)

app = Flask('__name__', template_folder="templates")

def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def scrape_google(query):

    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)

    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')
    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)
    return links

def emoccion(soup):
  try:
    tags = soup.find_all()
    word_count = {'html' : []}
    for tag in tags:
      tag_name = tag.name
      text = tag.get_text().strip()
      count = len(text.split())
      if tag_name in word_count:
        word_count.update({tag_name : count})
      else:
        word_count.update({tag_name : count})
    del word_count["html"]
    sorted_dict = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    potat = []
    for i in range(3):
      key, value = sorted_dict[i]
      potat.append(key)

    return potat
  except Exception as e:
    print("An error occurred: ", e)
    return None
  
def get_sentiment(query, sadness, joy, love, anger, fear, surprise):
    # Perform sentiment analysis and get scores
    # total = 100
    # pos = random.randint(0, total)
    # total -= pos
    # neg = random.randint(0, total)
    # neu = total - neg
    # url = news_url[random.randint(0, len(news_url))]
    sadness *= 100
    joy *= 100
    love *= 100
    anger *= 100
    fear *= 100
    surprise *= 100

    # Print results
    # print(f"Sentiment Scores for {url}:")
    # print(f"Positive: {pos}%")
    # print(f"Negative: {neg}%")
    # print(f"Neutral: {neu}%")

    # Set up plot
    labels = ['sadness','joy','love','anger','fear','surprise']
    sentiments = [sadness, joy, love, anger, fear, surprise]
    colors = ['red','yellow','blue','green','violet','#30D5C8']

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    # Plot bar chart
    axis.bar(labels, sentiments, color=colors)

        # Set chart title and labels
    # fig.title('Sentiment Analysis Results')
    # fig.xlabel('Sentiment')
    # fig.ylabel('Percentage')

    return fig

        # Display the chart
        # plt.show()
    # plt.savefig("output.jpg")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/print-plot' , methods = ['POST'])
def plot_png():
    if request.method == 'GET':
       return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        print("reached here")
        query=request.form['query']
        prediction = classifier(query)

        sadness = prediction[0][0]['score']
        joy = prediction[0][1]['score']
        love = prediction[0][2]['score']
        anger = prediction[0][3]['score']
        fear = prediction[0][4]['score']
        surprise = prediction[0][5]['score']

        
        fig = get_sentiment(query=query, sadness=sadness, joy=joy, love=love, anger=anger, fear=fear, surprise=surprise)
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')

        # get_sentiment(query, news_url=news_url)
    #return render_template("data.html", urls = news_url)
    # return render_template("analyze.html")

@app.route('/analyze', methods=['POST'])
def analyze():
   if request.method == 'GET':
       return f"The URL /data is accessed directly. Try going to '/form' to submit form"
   if request.method == 'POST':
    print("reached here")
    query=request.form['query']
    pot = scrape_google(query=query)
    news_url = []   
    for url in pot:
        if re.search(r"", url):
            news_url.append(url)
        else:
            print("Error...")
   


if __name__=="__main__":
    app.run()