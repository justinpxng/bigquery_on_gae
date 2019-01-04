import logging
import numpy as np

from flask import Flask, jsonify, render_template, request
from google.cloud import bigquery
from requests_toolbelt.adapters import appengine
appengine.monkeypatch()

app = Flask(__name__)


def query_stackoverflow(tag):
    client = bigquery.Client()
    query_job = client.query("""
        SELECT
          title,
          view_count
        FROM `bigquery-public-data.stackoverflow.posts_questions`
        WHERE tags like '%""" + tag + """%'
        ORDER BY view_count DESC
        LIMIT 10""")

    results = query_job.result()  # Waits for job to complete.
    results_dict = dict([ (row.title, row.view_count) for row in results ])
    
    return results_dict
                

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submitted_form', methods=['POST'])
def submitted_form():
    tag = request.form['tag']
    query_result = query_stackoverflow(tag)
    
    return render_template(
        'submitted_form.html',
        tag=tag,
        titles=query_result)
