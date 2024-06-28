from elasticsearch import Elasticsearch
from flask import Flask, render_template, request
import json

app = Flask(__name__)


client = Elasticsearch(
  "https://f935605f13ee463382d108587978eec1.us-central1.gcp.cloud.es.io:443",
  api_key="N1U3bFdaQUJTZkUza2t5UjcxNy06NjRJY3k1XzNScy1tN0VjcGJEaVM4Zw=="
)

with open('db\spans.json', 'r', encoding='utf-8') as f:
    documents = json.load(f)

# for i, doc in enumerate(documents):
#   client.index(index="test-index", id=i, document=doc)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        q = request.form['search']
        index = request.form['index']
        search_types = {
            'index_label': 'label_name',
            'index_sents': 'sentence'
        }
        body = {
                "query": {
                  "term": {
                    search_types[index]: q
                  }
                }
              }
        res = client.search(index='test-index', body=body)
        return render_template('base.html', res=res['hits']['hits'])
    else:
        return render_template('base.html', res={})

if __name__ == '__main__':
    app.run()