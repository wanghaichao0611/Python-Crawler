import requests
import concurrent.futures
import multiprocessing as mp
import lib.function.common as common


# download and write or [{'key':'1'},{'key':'2'] and [1,2.3.4.5.6]
# def download_ts(data):
#     print('Downloading: ' + data['download_url'])
#     response = requests.get(data['download_url'])
#     if response.status_code == 200:
#         with open(data['write_url'], 'wb') as r:
#             r.write(response.content)

def download_ts(download_url, write_url):
    print('Downloading: ' + download_url)
    response = requests.get(download_url)
    if response.status_code == 200:
        with open(write_url, 'wb') as r:
            r.write(response.content)


if __name__ == '__main__':
    data_list = common.read_data_list('../../out/twitch/twitch_ts.json')
    # with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
    #     executor.map(download_ts, data_list)
    #     executor.shutdown()
    with mp.Pool(mp.cpu_count()) as p:
        p.starmap(download_ts, data_list)
