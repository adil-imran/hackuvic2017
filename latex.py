from tex import latex2pdf
import os

final_doc = '''\documentclass [12pt] {article}
\usepackage{amsmath}
\makeatletter
\\renewcommand{\@seccntformat}[1]{}
\makeatother
\usepackage{url}
\usepackage[margin=0.8in]{geometry}
\pagestyle{plain}
\\begin{document}
\section*{Safe Newspaper for Kids} %(latex_tex)s \end{document}
'''


news_article = '''\subsection{%(article_heading)s}
\[
%(article_text)s
\]
'''

def createNewsPaper(articles):
    news =''
    for article in articles:
        news += (news_article % {'article_heading':article['heading'], 'article_text':article['text'].replace(' ', '\ ')})

    f = open('news.tex','w')
    f.write(final_doc % {'latex_tex':news})

    f.close()
    os.system("pdflatex news.tex")
