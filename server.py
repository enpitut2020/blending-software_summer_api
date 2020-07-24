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

@app.route("/personalized_pagerank", methods=["POST"])
def personalized_pagerank():
    """
    現段階では本当のページランクではなく、推薦するチャンネル情報が書き込まれたjsonを返す。
    チャンネル情報
      channel: channel_name (文字配列), 
      チャンネルホームURL: home_url (文字配列)
    """
    if request.method == "POST":
        ch_name = request.form["channel_name"]
        info_of_recommended_channel = {
                "channel_id1": ["SPYGEA", "https://www.youtube.com/user/jpspygea"],
                "channel_id2": ["YamatoN", "https://www.youtube.com/user/jpspygea"],
            }
        return jsonify(info_of_recommended_channel)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
