import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, jsonify
import networkx as nx

app = Flask(__name__)

def personalized_pagerank(ch_id=None):
    if ch_id == None:
        return False
    # グラフ作成
    G = nx.read_edgelist("data/edge_list.txt", delimiter=' , ')
    # pagerank計算
    pr = nx.pagerank(G, personalization={ch_id: 1})
    # 自分は除外
    del pr[ch_id]
    # ソートしてjsonにエンコード
    ids_of_recommended_channel = dict(sorted(pr.items(), key=lambda x: -x[1])[:5])
    return ids_of_recommended_channel

@app.route("/recommended_channels", methods=["POST"])
def recommended_channels():
    """
    推薦するチャンネル情報が書き込まれたjsonを返す。
    """
    if request.method == "POST":
        ch_name = request.form["channel_name"]
        ch_id = channel_name2channel_id(ch_name)
        if ch_id:
            ids_of_recommended_channel = personalized_pagerank(ch_id)
            infos_of_recommended_channel = []
            for id in ids_of_recommended_channel:
                info_of_recommended_channel = get_channel_info(id)
                infos_of_recommended_channel.append(info_of_recommended_channel)
            channel_used_for_search = get_channel_info(ch_id)["channel_name"]
            response = {"ans": infos_of_recommended_channel, "channel_name_used_for_search": channel_used_for_search}
        else:
            # POSTで送られたきたチャンネル名がdatabase.csvに登録されていなかった場合
            response = {"ans": []}

        return jsonify(response)

@app.route("/network_edge_data", methods=["GET"])
def network_edge_data():
    with open("data/edge_list.txt", "r") as f:
        text_edge_data = f.read()
        text_edge_data = text_edge_data.replace(" ", "").split("\n")
        edge_of_ch_id = [edge.split(",") for edge in text_edge_data if not edge == ""]

        # チャンネル名とチャンネルIDが紐付けられないデータがあるので確認
        edge_of_channel = []
        for e in edge_of_ch_id:
            edge = []
            node1 = get_channel_info(e[0])
            node2 = get_channel_info(e[1])
            if node1 and node2:
                edge.append(node1)
                edge.append(node2)
                edge_of_channel.append(edge)

        return jsonify({"edge": edge_of_channel})

def channel_name2channel_id(channel_name):
    df = pd.read_csv("data/database.csv")
    channel_id = df[df['channel_name'].str.contains(channel_name, case=False)].sort_values('subscriberCount', ascending=False)[0:1]['channel_id']
    if len(channel_id) == 0:
        return None
    else:
        return channel_id.values[0] # channel_id自体は1つだがSeriesになっているので要素を取り出す

def get_channel_info(channel_id):
    df = pd.read_csv("data/database.csv")
    df_channel_info = df[df["channel_id"]==channel_id]
    if len(df_channel_info) == 0:
        return None
    recommended_channel = {
            "channel_id": channel_id,
            "channel_name": df_channel_info["channel_name"].values[0],
            "channel_description": df_channel_info["channel_description"].values[0],
            "home_url": df_channel_info["home_url"].values[0],
            "thumbnail_url": df_channel_info["thumbnail_url"].values[0],
            "m_thumbnail_url": df_channel_info["m_thumbnail_url"].values[0],
            "h_thumbnail_url": df_channel_info["h_thumbnail_url"].values[0],
            "viewCount": str(df_channel_info["viewCount"].values[0]),
            "subscriberCount": str(df_channel_info["subscriberCount"].values[0]),
            "videoCount": str(df_channel_info["videoCount"].values[0]),
        }
    return recommended_channel

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
