# all the imports
import os 
import sqlite3 
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import newspaper
import atexit

app = Flask(__name__) # create the application instance 
app.config.from_object(__name__) # load config from this file

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'newsapp.db'),
    SECRET_KEY='development key', 
    USERNAME='admin', 
    PASSWORD='default'
))
app.config.from_envvar('NEWSAPP_SETTINGS',  silent=True)


## Database Stuff: 

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the 
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f: 
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initialize the database."""
    init_db()
    print('Initialized the database.')

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


## Fetch article stuff:

def get_news_articles():
    print("Fetching new articles...")

    # Get 10 aritcles from newspaper
    url = "http://cnn.com"
    paper = newspaper.build(url, memorize_articles=False,       
            keep_article_html=True) # caching off
    last_10 = paper.articles[-10:] # get 10 most recent articles


    articles = []
    for article in last_10:
        article.download()
        article.parse()
        authors = ",".join(article.authors)
        articles.append([article.url, authors, article.title, 
                         article.text, article.top_image])

    print(articles)

    # Store them in the db
    db = get_db()
    for article in articles: 
        db.execute('insert into articles(url, title, author, content, '
                   'thumbnail) values (?, ?, ?, ?, ?)', 
                   [article[0], article[2], article[1], article[3],
                    article[4]])
        db.commit()
    flash('Updated the articles in the db (the real ones)')


@app.before_first_request
def initialize():
    get_news_articles() # initial request
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=get_news_articles,
        trigger=IntervalTrigger(hours=1),
        id='get_news_articles_job',
        name='Get news articles every hour', 
        replace_existing=True)
    atexit.register(lambda: scheduler.shutdown())
    
    

## Views stuff:

@app.route('/')
def show_articles():
    db = get_db()
    cur = db.execute('select url, title, author, content from articles order by id desc')
    articles = cur.fetchall()
    return render_template('show_articles.html', articles=articles)

@app.route('/get')
def get_articles():
    db = get_db()
    db.execute('insert into articles (url, title, author, content, ' 
                'thumbnail) values (?, ?, ?, ?, ?)',
        ['http://www.example.com',
        'Example Title', 
        'Author Name 1, Author Name 2', 
        '<p>This is the <strong>HTML</strong> content of an article</p>',
        'https://www.example.com']
    )
    db.commit() 
    flash('Updated the articles in the db')
    return redirect(url_for('show_articles'))



