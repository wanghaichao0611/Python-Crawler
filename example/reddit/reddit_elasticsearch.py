import json
import os
from dotenv import load_dotenv
from conf.settings import DATABASES
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

load_dotenv(dotenv_path="../../env/learning.env", override=True)
es = Elasticsearch(hosts=DATABASES.get('elasticsearch').get('host'))
reddit_into_file = os.environ.get('reddit_into_file')

docs = [
    {
        '_index': 'test_es',
        '_source': {
            'title': 'title one',
            'content': 'content one',
            'author': 'author one'
        }
    },
    {
        '_index': 'test_es',
        '_source': {
            'title': 'title two',
            'content': 'content two',
            'author': 'author two'
        }
    }
]


# send elasticsearch for a test
def send_data_test(data_list):
    bulk(es, data_list)
    print('send test successfully')


# read local json file
def read_data_list(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)


# send data to elasticsearch
def send_data_to_elasticsearch(data_list, index):
    docs = []
    for data in data_list:
        docs.append({
            '_index': 'reddit_top_year',
            '_source': data})

    # batch into elasticsearch
    bulk(es, docs)
    print('send data to elasticsearch successfully')


# get dta from elasticsearch with query
def get_data_from_elasticsearch(index, words):
    query = {
        "query": {
            "match": {'content': words}
        }
    }
    value = es.search(index=index, body=query)
    print(value)


# main
if __name__ == '__main__':
    # send_data_test(docs)
    # get_data_from_elasticsearch('reddit_top_year', 'happy')
    # es.indices.delete(index='reddit_top_year')
    send_data_to_elasticsearch(read_data_list('../../out/reddit/' + reddit_into_file), 'reddit_top_year')
