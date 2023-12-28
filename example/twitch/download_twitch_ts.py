import requests
import concurrent.futures
import lib.function.common as common


# download and write
def download_ts(data):
    response = requests.get(data['download_url'])
    if response.status_code == 200:
        with open(data['write_url'], 'wb') as r:
            r.write(response.content)


if __name__ == '__main__':
    data_list = common.read_data_list('../../out/twitch/twitch_ts.json')
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        executor.map(download_ts, data_list)
        executor.shutdown()
