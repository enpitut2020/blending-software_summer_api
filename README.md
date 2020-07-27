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

## テスト用コマンド
```
curl -X POST -F 'channel_name=兄者弟者' https://youtuber-search-api.herokuapp.com/recommended_channels
```

