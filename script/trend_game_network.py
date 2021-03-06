import os
import csv
import pandas as pd
from apiclient.discovery import build


def get_popular_videos(youtube):
    return youtube.videos().list(
        part='id,snippet',
        chart='mostPopular',
        regionCode='JP',
        videoCategoryId='20',
        maxResults='5',
    ).execute()


def get_related_videos(youtube, channelId_set, res, edge_list, dep=1, m=5, first_flag=True):
    for item in res['items']:
        search_response = youtube.search().list(
            part='id,snippet',
            relatedToVideoId=item['id'] if first_flag else item['id']['videoId'],
            type='video',
            videoCategoryId='20',
            maxResults=m,
        ).execute()

        for i in search_response['items']:
            if(item['snippet']['channelId'] != i['snippet']['channelId']):
                tmp = []
                tmp.append(item['snippet']['channelId'])
                tmp.append(i['snippet']['channelId'])
                edge_list.append(tmp)
                channelId_set.add(i['snippet']['channelId'])

        # depが１より大きければ再帰処理
        if(dep > 1):
            edge_list.extend(get_related_videos(youtube, channelId_set, search_response, edge_list, dep=dep - 1, first_flag=False))

    return edge_list


def write_channel_info(youtube, channelId_set, path, writing_type):
    channelIds_str = ','.join(map(str, channelId_set))
    print(channelIds_str)
    print(len(channelIds_str))

    channels = youtube.channels().list(
            part='snippet',
            id=channelIds_str
            ).execute()

    with open(path, writing_type) as f:
        writer = csv.writer(f)
        if writing_type == 'w':
            writer.writerow(["channel_id", "channel_name", "home_url", "thumbnail_url"])
        for channel in channels['items']:
            writer.writerow([
                channel["id"],
                channel['snippet']['title'],
                "https://www.youtube.com/channel/" + channel['id'],
                channel['snippet']['thumbnails']['default']['url']
                ])

    # 重複削除
    # if writing_type == 'a':
    #     df = pd.read_csv("data/database.csv")
    #     df.drop_duplicates(inplace=True)
    #     df.to_csv(path)


if __name__ == '__main__':

    # API_KEYを設定
    YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    edge_list = []
    channelId_set = set()
    # 人気動画取得
    popular_videos = get_popular_videos(youtube)
    for item in popular_videos['items']:
        channelId_set.add(item['snippet']['channelId'])

    # 関連動画取得
    edge_list = get_related_videos(youtube, channelId_set,popular_videos, edge_list, m=3, dep=2)

    # 重複削除
    edge_list = list(map(list, set(map(tuple, edge_list))))

    with open('data/edge_list.txt', 'w') as f:
        for list in edge_list:
            s = ' , '.join(list)
            f.write(s + "\n")


    # チャンネル情報書き込み
    write_channel_info(youtube, channelId_set, "data/database.csv", 'w')
