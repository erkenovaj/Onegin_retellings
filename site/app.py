from elasticsearch import Elasticsearch
from flask import Flask, render_template, request
import json
from getpass import getpass

app = Flask(__name__)

client = Elasticsearch(
  "https://f935605f13ee463382d108587978eec1.us-central1.gcp.cloud.es.io:443",
  api_key="TUJqa1g1QUJ5TnR1Sm5meHg1UDU6OHRZTzBFWTFTeUNDa2ViLVo5MjVnZw=="
)

# with open('db\spans.json', 'r', encoding='utf-8') as f:
#   documents = json.load(f)

# for i, doc in enumerate(documents):
#   client.index(index="onegin", id=i, document=doc)

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
                  "match": {
                    search_types[index]: q
                  }
                }
              }
        res = client.search(index='onegin', body=body)
        return render_template('base.html', res=res['hits']['hits'], search_query=q, selected_index=index)
    else:
        return render_template('base.html', res={}, search_query='', selected_index='')

if __name__ == '__main__':
    app.run()