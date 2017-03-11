from flask import Flask, render_template
import newspaper
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import datetime
import atexit

app = Flask(__name__)

def get_news_articles():
    print("Fetching new articles...")
    return ["first {0}".format(datetime.datetime.now()), 
            "second {0}".format(datetime.datetime.now()), 
            "third {0}".format(datetime.datetime.now())]

@app.before_first_request
def initialize():
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func = get_news_articles,
        trigger=IntervalTrigger(seconds=5),
        id='get_news_articles_job',
        name='Get news articles every 3600 seconds',
        replace_existing=True)
    atexit.register(lambda: scheduler.shutdown())

@app.route("/")
def hello():
    headlines = ['first headline', 'second headline', 'third  headline']
    return render_template('home.html', headlines=headlines)


if __name__ == "__main__":
    app.run()
