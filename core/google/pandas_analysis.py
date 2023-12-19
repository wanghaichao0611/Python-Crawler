import matplotlib
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import lib.function.common as common

matplotlib.use('TkAgg')


def main():
    excel = pd.read_excel('F:\GitHubProject\Python-Crawler\out\google\Twitch.xlsx', index_col=0)
    excel.sort_values(by='peoples', inplace=True, ascending=False)
    data = pd.DataFrame(excel)
    print(data.describe())
    print(data.shape)
    print(data)
    data_temp = data[:25]
    # for index, row in data_temp.iterrows():
    #     plt.text(x=row['author_name'], y=row['peoples'], s=str(row['peoples']),
    #              color='black', fontsize=12, style='normal', ha='center')
    # data.plot.bar(x='author_name', rot=0, edgecolor='grey', colormap='rainbow')
    sns.barplot(data_temp, x="author_name", y='peoples', hue='author_name', saturation=0.2)
    plt.title('Twitch Top Online', fontsize=20)
    common.adjust_plt()
    plt.xticks(rotation=45, ha='right')
    plt.savefig('../../out/google/TopPeoples.pdf')
    plt.show()


if __name__ == '__main__':
    main()
