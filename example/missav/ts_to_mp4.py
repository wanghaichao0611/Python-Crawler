import os
import datetime
from dotenv import load_dotenv

load_dotenv(dotenv_path="../../env/learning.env", override=True)

av_video_path = os.environ.get('av_video_path')
av_mp4_path = os.environ.get('av_mp4_path')


def main(path, save_path):
    file_names = os.listdir(path)
    for folder in file_names:
        folder_names = os.listdir(path + folder)
        # if 'file_list.txt' in file_names:
        #     os.remove(path + folder + '\\file_list.txt')
        out_file_name = folder + '.mp4'
        # while out_file_name in os.listdir(save_path):
        #     out_file_name = '新' + out_file_name
        f = open(path + folder + '\\file_list.txt', 'w+')
        # print(folder_names)
        for one in folder_names:
            f.write("file '" + one + "'\n")
            # print(one)
        f.close()
        print("生成txt文件成功!")
        start = datetime.datetime.now()
        print('开始合成，初始时间为:', datetime.datetime.now())
        # download /bin/ffmpeg
        ffmpeg_bin_dic = 'F:\\ffmpeg\\bin\\'
        os.system(
            ffmpeg_bin_dic + 'ffmpeg -f concat -safe 0 -i ' + path + folder + '\\file_list.txt' + ' -c ' + ' copy '
            + save_path + out_file_name)

        print('合成后的当前时间为：', datetime.datetime.now())
        print('合成视频完成！用时：' + str(datetime.datetime.now() - start))


if __name__ == '__main__':
    main(av_video_path, av_mp4_path)
