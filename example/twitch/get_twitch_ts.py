import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../../env/learning.env", override=True)

twitch_user_videos = os.environ.get('twitch_user_videos')
twitch_user = os.environ.get('twitch_user')
twitch_user_out_path = os.environ.get('twitch_user_out_path')
twitch_video_path = os.environ.get('twitch_video_path')
twitch_mp4_path = os.environ.get('twitch_mp4_path')
twitch_720 = os.environ.get('twitch_720')


# load twitch_user_json
def read_json_list(genshin_impact):
    with open(genshin_impact, 'r', encoding='utf-8') as f:
        return json.load(f)


# get_video_st
def get_video_ts(data_list):
    ts_list = []
    for data in data_list:
        count = 0
        count_split = data['count_split']
        while count < count_split:
            name = count
            next = len(str(count_split)) - len(str(count))
            if next > 0:
                if next == 1:
                    name = '0' + str(count)
                if next == 2:
                    name = '00' + str(count)
                if next == 3:
                    name = '000' + str(count)
                if next == 4:
                    name = '0000' + str(count)
            download_url = 'https://' + data['split_front'] + '.cloudfront.net/' + data[
                'split_author'] + '/' + twitch_720 + '/' + str(count) + '.ts'
            write_url = twitch_video_path + data['img_title'] + '//' + str(name) + '.ts'
            # ts_list.append({'download_url': download_url, 'write_url': write_url})
            ts_list.append((download_url, write_url))
            count += 1

    with open('../../out/twitch/twitch_ts.json', "w", encoding='utf-8') as json_list:
        json.dump(ts_list, json_list)


if __name__ == '__main__':
    print('start split ts')
    get_video_ts(read_json_list(twitch_user_out_path))
    print('end split ts')
