from flask import Flask, render_template, g
import newspaper
import classifier

app = Flask(__name__)

def get_news_articles(url):
	paper = newspaper.build(url, memoize_articles=False, keep_article_html=True) # caching off
	last_10 = paper.articles[-10:] # get 10 most recent articles

	articles = []
	for article in last_10:
		article.download()
		article.parse()
		authors = ", ".join(article.authors)
		articles.append([article.url, authors, article.title, article.text, article.top_image])

	return articles

#@app.before_first_request
def article_classifier(articles):
	c = classifier.ArticleClassifier()
	return c.classify(articles)

@app.route("/")
def hello():
	articles = get_news_articles('http://cnn.com') # each article is ['url', [authors], 'headline', 'text']
	article_text = [a[3] for a in articles]
	article_classified = article_classifier(article_text)
	new = []
	for a, b in zip(articles, article_classified):
		a.append(b)
	return render_template('home.html', articles=articles)

if __name__ == "__main__":
	app.run()
