import logging
import numpy as np

from flask import Flask, jsonify, render_template, request
from google.cloud import bigquery
from requests_toolbelt.adapters import appengine
appengine.monkeypatch()

app = Flask(__name__)


def query_stackoverflow():
    client = bigquery.Client()
    query_job = client.query("""
        SELECT
          CONCAT(
            'https://stackoverflow.com/questions/',
            CAST(id as STRING)) as url,
          view_count
        FROM `bigquery-public-data.stackoverflow.posts_questions`
        WHERE tags like '%google-bigquery%'
        ORDER BY view_count DESC
        LIMIT 10""")

    results = query_job.result()  # Waits for job to complete.
    results_dict = dict([ (row.url, row.view_count) for row in results ])
    
    return jsonify(results_dict)
                

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submitted', methods=['POST'])
def submitted_form():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']

    return render_template(
        'submitted_form.html',
        name=name,
        email=email,
        site=site,
        comments=comments)

@app.route('/bq')
def bq():
    return query_stackoverflow()
