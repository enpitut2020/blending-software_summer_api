import os
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        ch_id = request.form['ch_id']
        url = f'http://localhost:5000/personalized_pagerank/{ch_id}'
        response = requests.get(url)
        return response

@app.route(f'/personalized_pagerank/<ch_id>', methods=['GET'])
def personalized_pagerank(ch_id=None):
    """
    現段階では本当のページランクではなく、推薦するチャンネルのIDが保存されたjsonを返す。
    チャンネルIDは以下のようにURLに含まれる
    youtube.com/user/チャンネルID  (チャンネルのホームページのURL)
    """
    ids_of_recommended_channel = {"ch_id": ["jpspygea", "YamatoNjp", "Poulmt", "vodkaplaysful"]}
    return jsonify(ids_of_recommended_channel)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))