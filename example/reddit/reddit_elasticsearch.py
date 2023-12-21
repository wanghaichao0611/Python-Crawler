import json
from conf.settings import DATABASES
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

es = Elasticsearch(hosts=DATABASES.get('elasticsearch').get('host'))

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


def send_data_test(data_list):
    bulk(es, data_list)
    print('send test successfully')


def read_data_list(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)


def send_data_to_elasticsearch(data_list, index):
    docs = []
    for data in data_list:
        docs.append({
            '_index': 'reddit_top_year',
            '_source': data})

    bulk(es, docs)
    print('send data to elasticsearch successfully')


def get_data_from_elasticsearch(index, words):
    query = {
        "query": {
            "match": {'content': words}
        }
    }
    value = es.search(index=index, body=query)
    print(value)


if __name__ == '__main__':
    # send_data_test(docs)
    # get_data_from_elasticsearch('reddit_top_year', 'happy')
    # es.indices.delete(index='reddit_top_year')
    send_data_to_elasticsearch(read_data_list('../../out/reddit/genshin_impact_top.json'), 'reddit_top_year')
