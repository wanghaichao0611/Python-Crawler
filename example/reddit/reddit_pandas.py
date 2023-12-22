import matplotlib
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import lib.constant.globals as constant
import lib.function.common as common
import json
from conf.settings import DATABASES
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from pylab import mpl

mpl.rcParams["font.sans-serif"] = ["SimHei"]
mpl.rcParams["axes.unicode_minus"] = False

es = Elasticsearch(hosts=DATABASES.get('elasticsearch').get('host'))
matplotlib.use('TkAgg')


# load genshin_impact.json
def read_json_list(genshin_impact):
    with open(genshin_impact, 'r', encoding='utf-8') as f:
        return json.load(f)


# get count words from elasticsearch with query
def get_count_words_from_elasticsearch(index, words):
    query = {
        "query": {
            "multi_match": {
                "query": words,
                "fields": ["title", "content"]
            }

        }
    }
    value = es.search(index=index, body=query)
    return int(value['hits']['total']['value'])


# start
def main():
    data_list = {}
    genshin_impact_list = read_json_list('../../example/reddit/genshin_impact.json')
    for key, value in genshin_impact_list.items():
        data_list[key] = []
        inner_list = []
        for name in value:
            count = get_count_words_from_elasticsearch('reddit_top_year', name)
            # print(name + ': ' + count.__str__())
            inner_list.append([name, count])
            data_list[key].append((name, count))

        data = pd.DataFrame(inner_list, columns=['name', 'count']).sort_values(by='count', ascending=False)
        sns.barplot(y='name', x="count", data=data, hue='name', saturation=0.2)
        plt.title(key, fontsize=20)
        common.adjust_plt()
        plt.xticks(rotation=90, ha='right')
        print(str(key).split('-')[0].strip())
        plt.savefig('../../out/reddit/pandas/' + str(key).split('-')[0].strip() + '.jpg', dpi=200, bbox_inches='tight')
        plt.close()

    with open('../../out/reddit/pandas/pandas.json', "w", encoding='utf-8') as json_list:
        json.dump(data_list, json_list, ensure_ascii=False)


if __name__ == '__main__':
    main()
