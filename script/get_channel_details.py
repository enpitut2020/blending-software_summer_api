import os
import csv
import pandas as pd
from apiclient.discovery import build

def write_channel_info(youtube, channelId_set, path):
    # channelIds_str = ",".join(map(str, channelId_set))
    # channelId_list = list(channelId_set)
    # channels = youtube.channels().list(
    #         part='snippet,statistics',
    #         # id=channelIds_str
    #         id=channelId_list
    #         ).execute()

    with open(path,'w') as f:
        writer = csv.writer(f)
        writer.writerow([
            "channel_id",
            "channel_name",
            "channel_description",
            "home_url",
            "thumbnail_url",
            "m_thumbnail_url",
            "h_thumbnail_url",
            "viewCount",
            "subscriberCount",
            "videoCount",
            ])

        for channelId in channelId_set:
            channels = youtube.channels().list(
                    part='snippet,statistics',
                    id=channelId
                    ).execute()

            for channel in channels['items']:
                writer.writerow([
                    channel["id"],
                    channel['snippet']['title'],
                    repr(channel['snippet']['description']),
                    "https://www.youtube.com/channel/" + channel['id'],
                    channel['snippet']['thumbnails']['default']['url'],
                    channel['snippet']['thumbnails']['medium']['url'],
                    channel['snippet']['thumbnails']['high']['url'],
                    channel['statistics']['viewCount'],
                    channel['statistics']['subscriberCount'],
                    channel['statistics']['videoCount'],
                    ])

    # 重複削除
    # if writing_type == 'a':
    #     df = pd.read_csv("data/database.csv")
    #     df.drop_duplicates(inplace=True)
    #     df.to_csv(path)

def get_channelIds(path):
    channelIds = set()
    with open(path, 'r') as f:
        s = f.readline()
        while s:
            line = s.split()
            line.remove(',')
            channelIds.update(set(line))
            s = f.readline()

    return channelIds


if __name__ == '__main__':
    # API_KEYを設定
    YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    channelId_set = get_channelIds('data/edge_list.txt')
    write_channel_info(youtube, channelId_set, "data/database.csv")
