import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, jsonify
import networkx as nx

app = Flask(__name__)

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        ch_id = request.form['ch_id']
        url = f'http://localhost:5000/personalized_pagerank/{ch_id}'
        response = requests.get(url)
        return response

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
    現段階では本当のページランクではなく、推薦するチャンネル情報が書き込まれたjsonを返す。
    """
    if request.method == "POST":
        ch_name = request.form["channel_name"]
        ch_id = channel_name2channel_id(ch_name)
        ids_of_recommended_channel = personalized_pagerank(ch_id)
        infos_of_recommended_channel = []
        for id in ids_of_recommended_channel:
            info_of_recommended_channel = get_recommended_channel(id)
            infos_of_recommended_channel.append(info_of_recommended_channel)

        response = {"ans": infos_of_recommended_channel}
        return jsonify(response)

def channel_name2channel_id(channel_name):
    df = pd.read_csv("data/database.csv")
    #print(df)
    print(df[df["channel_name"]==channel_name]["channel_id"])
    channel_id = df[df["channel_name"]==channel_name]["channel_id"].values[0]
    return channel_id

def get_recommended_channel(channel_id):
    df = pd.read_csv("data/database.csv")
    print(channel_id)
    df_recommended_channel = df[df["channel_id"]==channel_id]
    recommended_channel = {
            "channel_id": channel_id,
            "channel_name": df_recommended_channel["channel_name"].values[0],
            "home_url": df_recommended_channel["home_url"].values[0],
            "thumbnail_url": df_recommended_channel["thumbnail_url"].values[0]
        }
    return recommended_channel

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
