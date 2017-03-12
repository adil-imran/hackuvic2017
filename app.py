from flask import Flask, render_template
import newspaper
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import datetime
import atexit

app = Flask(__name__)

"""def get_news_articles():
    print("Fetching new articles...")
    return ["first {0}".format(datetime.datetime.now()), 
            "second {0}".format(datetime.datetime.now()), 
            "third {0}".format(datetime.datetime.now())]"""

def get_news_articles(url):
	paper = newspaper.build(url, memoize_articles=False, keep_article_html=True) # caching off
	last_10 = paper.articles[-10:] # get 10 most recent articles

	articles = []
	for article in last_10:
		article.download()
		article.parse()
		articles.append([article.url, article.authors, article.title, article.article_html])

	return articles

"""@app.before_first_request
def initialize():
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func = get_news_articles,
        trigger=IntervalTrigger(seconds=5),
        id='get_news_articles_job',
        name='Get news articles every 3600 seconds',
        replace_existing=True)
    atexit.register(lambda: scheduler.shutdown())"""

@app.route("/")
def hello():
	articles = get_news_articles('http://cnn.com') # each article is ['url', [authors], 'headline', 'text']
    return render_template('home.html', articles=articles)


if __name__ == "__main__":
    app.run()
