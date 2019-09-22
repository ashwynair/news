#!/usr/bin/env python3

# Log analysis project.

from flask import Flask, request, redirect, url_for
from psycopg2 import connect

app = Flask(__name__)

# HTML template for the logs analysis page
HTML_WRAP = '''\
<!DOCTYPE html>
<html>
    <head>
        <style>
            body {
                -webkit-font-smoothing: antialiased;
                }
            h1, p, ul {font-family: Helvetica,Open Sans,sans-serif;}
            p.question {font-weight:bold;}
            li {
                display: list-item;
                list-style-type: disc;
                margin-top: 0.5em;
                margin-bottom: 0.5em;
                margin-left: 0;
                margin-right: 0;
                }
        </style>
    <head>
        <title>Logs Analysis</title>
    </head>
    <body>
        <h1>Logs Analysis</h1>
        <p class = "question">
            1. What are the most popular three articles of all time?
        </p>
        <ul>
            %s
        </ul>
        <p class = "question">
            2. Who are the most popular article authors of all time?
        </p>
        <ul>
            %s
        </ul>
        <p class = "question">
            3. On which days did more than 1%% of requests lead to errors?
        </p>
        <ul>
            %s
            </ul>
    </body>
</html>
'''

# HTML templates for each answer
ANSWER = (
    '''<li>"%s" — %s views</li>''',
    '''<li>%s — %s views</li>''',
    '''<li>%s — %s errors</li>'''
)

# Database and view names
DBNAME = "news"
VIEWS = ("popular_articles", "popular_authors", "one_perc_error_days")


@app.route('/', methods=['GET'])
def main():
    '''Main page of the logs analysis.'''
    raw_answers = get_posts()
    answers = []
    for i in range(len(raw_answers)):
        answers.append("".join(ANSWER[i] % (a, b) for a, b in raw_answers[i]))
    html = HTML_WRAP % tuple(answers)
    return html

# 
def get_posts():
    '''Return answers for each question from pre-defined views.'''
    db = connect(database=DBNAME)
    c = db.cursor()
    answers = []
    for i in range(len(VIEWS)):
        c.execute("select * from " + VIEWS[i] + ";")
        answers.append(c.fetchall())
    db.close()
    return tuple(answers)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
