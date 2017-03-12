from flask import Flask
import newspaper
app = Flask(__name__)

def get_news_articles(url):
	paper = newspaper.build(url, memoize_articles=False) # caching off
	last_10 = paper.articles[-10:] # get 10 most recent articles

	articles = []
	for article in last_10:
		article.download()
		article.parse()
		articles.append([article.url, article.authors, article.title, article.text])

	return articles

@app.route('/')
def main():
	articles = get_news_articles('http://cnn.com')
	a = newspaper.Article(articles[0][0], keep_article_html=True)
	a.download()
	a.parse()
	return a.article_html