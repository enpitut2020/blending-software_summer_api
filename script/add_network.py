import os
import csv
import sys
import pandas as pd
from trend_game_network import *
from apiclient.discovery import build


def get_popular_videos_by_ch_id(youtube, ch_id):
    channel = youtube.channels().list(
        part='contentDetails',
        id=ch_id
    ).execute()

    playlist_items = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=channel["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"],
        maxResults=10
    ).execute()

    videos = {"items": []}
    for item in playlist_items["items"]:
        print(item)
        videos["items"].append({"id": item["contentDetails"]["videoId"], "snippet": {"channelId": ch_id}})

    return videos


def add_network(youtube, ch_id):
    # チャンネルIDから人気動画を取得
    popular_video = get_popular_videos_by_ch_id(youtube, ch_id)

    # 関連動画取得
    edge_list = []
    channelId_set = set()
    channelId_set.add(ch_id)
    edge_list = get_related_videos(youtube, channelId_set, popular_video, edge_list, m=5, dep=1)

    # 重複削除
    edge_list = list(map(list, set(map(tuple, edge_list))))

    with open('data/edge_list.txt', 'a') as f:
        for e in edge_list:
            s = ' , '.join(e)
            f.write(s + "\n")

    # チャンネル情報書き込み
    write_channel_info(youtube, channelId_set, "data/database.csv", 'a')


if __name__ == '__main__':

    # API_KEYを設定
    YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    args = sys.argv
    add_network(youtube, args[1])
