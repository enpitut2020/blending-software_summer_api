import os
import csv
import pandas as pd
from apiclient.discovery import build

def write_channel_info(youtube, channelId_set, path):
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
                    repr(channel['snippet']['title']),
                    repr(channel['snippet']['description']),
                    "https://www.youtube.com/channel/" + channel['id'],
                    channel['snippet']['thumbnails']['default']['url'],
                    channel['snippet']['thumbnails']['medium']['url'],
                    channel['snippet']['thumbnails']['high']['url'],
                    channel['statistics']['viewCount'],
                    channel['statistics']['subscriberCount'],
                    channel['statistics']['videoCount'],
                    ])

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
