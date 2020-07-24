import os
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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
