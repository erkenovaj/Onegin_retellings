from elasticsearch import Elasticsearch
from flask import Flask, render_template, request
import json

app = Flask(__name__)


client = Elasticsearch(
  "https://ff50edc582264643a4b2cd2ea5b4ba22.us-central1.gcp.cloud.es.io:443",
  api_key="VUpUVkpwQUJyVGNGVkJoWHBJSkE6aUtKa3pMZHdRS0N5WXpPZ0t5SUdDQQ=="
)

documents = [
  { "index": { "_index": "index_name", "_id": "7"}},
  {"_id": "ObjectId('6673513eac128b59cf8c5cda')",
  "span": " Евгения Онегина.",
  "label_name": "full_name",
  "left_context": "И он расстроенный уходит, на этом наш роман кончается и что вы об этом думаете, как бы сами делайте выводы, как говорится, вот, спасибо.",
  "right_context": "В начале романа Евгений Онегин нам предстает частым гостем богемской тусовки Питера.",
  "sentence": "Пересказ Евгения Онегина.",
  "sentence_id": 1,
  "text_id": "ObjectId('6673513eac128b59cf8c5cd9')"},
  { "index": { "_index": "index_name", "_id": "8"}},
  {
  "span": " точнее",
  "label_name": "slang",
  "left_context": "Он ходит на все балы, на все обеды, на все представления в театре, то есть он уже там как свой.",
  "sentence": "Онегина пересказ",
  "right_context": "Для него женщины это просто ачивки, которые он хочет завоевать.",
  "text_id": "ObjectId('6673513eac128b59cf8c5cd9')",
  "sentence_id": 4},
  { "index": { "_index": "index_name", "_id": "9"}},
  {  "span": " присыпал",
  "label_name": "slang",
  "left_context": "Также у него были достаточно поверхностные знания, но этих поверхностных знаний ему было достаточно, чтобы в обществе он казался умным.",
  "right_context": "И из этого получился, получился вид таких глубоких начитанных знаний.",
  "sentence": "Точнее, эти поверхностные знания он также присыпал немножко харизмой и потом сверху чуть-чуть обаянием.",
  "text_id": "ObjectId('6673513eac128b59cf8c5cd9')",
  "sentence_id": 12},
  { "index": { "_index": "index_name", "_id": "10"}},
  {
  "span": " у него случился кризис четверти века.",
  "label_name": "interesting",
  "left_context": "И из этого получился, получился вид таких глубоких начитанных знаний.",
  "right_context": "И теперь он не понимает, что ему делать дальше.",
  "sentence": "Но, к сожалению, к своим 26 годам он понял, что все это ему надоело, а точнее у него случился кризис четверти века.",
  "text_id": "ObjectId('6673513eac128b59cf8c5cd9')",
  "sentence_id": 14}
]


client.bulk(operations=documents)
print(documents)

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
        res = client.search(index='index_name', body=body)
        return render_template('base.html', res=res['hits']['hits'])
    else:
        return render_template('base.html', res={})

if __name__ == '__main__':
    app.run()