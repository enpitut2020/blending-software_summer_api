# blending-software_summer_api
## 
## BaseURL
```
https://youtuber-search-api.herokuapp.com/
```
## おすすめチャンネルの取得
```
POST /recommended_channels
```
### Parameters
| Name | Type | Description |
| ---- | ---- | ---- |
|  channel_name  | string | おすすめのチャンネルが知りたいチャンネル名 |



## 配信者の関係を表すネットワークのエッジ情報の取得
```
GET /network_edge_data
```

## テスト用コマンド
### おすすめチャンネルの取得
```
curl -X POST -F 'channel_name=兄者弟者' https://youtuber-search-api.herokuapp.com/recommended_channels
```
### エッジ情報の取得
```
curl -X GET https://youtuber-search-api.herokuapp.com/network_edge_data
```

### Database
| channel_id | channel_name | channel_description | home_url | thumbnail_url | m_thumbnail_url | h_thumbnail_url | viewCount | subscriberCount | videoCount |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| チャンネルのid | チャンネル名 | チャンネル説明 | チャンネルのURL | サムネイルURL | サムネイルURL(中画質) | サムネイルURL(高画質) | 総視聴回数 | チャンネル登録者数 | ビデオ数 |
